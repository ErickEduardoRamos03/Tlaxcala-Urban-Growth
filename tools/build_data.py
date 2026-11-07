# -*- coding: utf-8 -*-
"""
Genera el dataset JSON que consume el portal Vue.js (web/).

Fuentes (todas dentro de data/, ya versionadas en el repo):
  - ITER 2010 / 2020  -> poblacion, foraneos, vivienda por municipio
  - DENUE 2010/2023/2024/2025 -> unidades economicas por municipio
  - GeoJSON INEGI (gaia) -> geometria municipal simplificada

Salida: web/src/data/datos.json

Uso:  python tools/build_data.py
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
import unicodedata
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(10**9)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CACHE = ROOT / "tools" / ".cache"
OUT = ROOT / "web" / "src" / "data" / "datos.json"

GEOJSON_URL = "https://gaia.inegi.org.mx/wscatgeo/v2/geo/mgem/29"
GEOJSON_CACHE = CACHE / "municipios_tlaxcala.geojson"

# Tolerancia de simplificacion en grados (~90 m). Ajuste de tamano del payload.
TOLERANCIA = 0.0008
# Lado de la celda de densidad en grados (~550 m).
CELDA = 0.005

# Palabras clave de las actividades "alimentos y bebidas".
# Mismo criterio EXACTO que usa el notebook: subcadena sin distinguir
# mayusculas y SIN normalizar acentos. Normalizar acentos daria falsos
# positivos ("Servicios de preparacion de documentos" contaria como comida).
KEYWORDS = ["CAFE", "RESTAURANTE", "BAR", "ALIMENTOS", "BEBIDA", "PREPARACION"]

# El DENUE 2010 usa tres grafias que difieren de los nombres oficiales
# vigentes del Marco Geoestadistico. Se normalizan por nombre normalizado.
ALIAS_MUNICIPIO = {
    "ALTZAYANCA": "ATLTZAYANCA",
    "YAUHQUEMECAN": "YAUHQUEMEHCAN",
    "ZITLALTEPEC DE TRINIDAD SANCHEZ SANTOS": "ZILTLALTEPEC DE TRINIDAD SANCHEZ SANTOS",
}

# DENUE: (zip, miembro, etiqueta de anio)
#
# Solo se usan 2010 y 2025 como cortes comparables. Los snapshots intermedios
# que trae el repo (nov-2023, may-2024, nov-2024) se descartan a proposito:
# al publicar cada edicion, DENUE reescribe masivamente el campo `fecha_alta`,
# de modo que el paso de 83,021 a 97,544 registros entre may-2024 y nov-2024
# no es crecimiento real de establecimientos sino reclasificacion masiva
# (~14,800 altas de 2019 reestampadas como 2024). Compararlos produziria una
# serie de crecimiento artificial.
DENUE_ARCHIVOS = [
    ("denue_29_2010_csv.zip", "DenueCSV29.csv", "2010"),
    ("denue_29_csv.zip", "conjunto_de_datos/denue_inegi_29_.csv", "2025"),
]

# SHF: indice de precios de vivienda, cierre 2025.
SHF = {"Tlaxcala": 12.0, "Nacional": 8.7}

# Cifras publicadas en el notebook (celda 18) que el portal debe reproducir.
VALIDACION_PUBLICADA = {
    "TLAXCALA": dict(alim2010=1437, alim2025=2127, pct=48.016701, pob2010=89795, pob2020=99896, foraneo=4.568752),
    "APIZACO": dict(alim2010=1523, alim2025=1882, pct=23.571898, pob2010=76492, pob2020=80725, foraneo=4.128832),
    "CHIAUTEMPAN": dict(alim2010=1222, alim2025=1727, pct=41.325696, pob2010=66149, pob2020=73215, foraneo=2.174418),
    "HUAMANTLA": dict(alim2010=1079, alim2025=1693, pct=56.904541, pob2010=84979, pob2020=98764, foraneo=2.448260),
}


# ---------------------------------------------------------------- utilidades
def normaliza(s: str) -> str:
    """Mayusculas, sin acentos, espacios colapsados. Solo para nombres propios."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().upper()


def coincide_actividad(act: str) -> bool:
    """Criterio identico al notebook: subcadena, sin distinguir mayusculas,
    conservando los acentos."""
    if not act:
        return False
    a = act.upper()
    return any(k in a for k in KEYWORDS)


def _dist2_point_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return (px - ax) ** 2 + (py - ay) ** 2
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    cx, cy = ax + t * dx, ay + t * dy
    return (px - cx) ** 2 + (py - cy) ** 2


def _dp_rec(xs, ys, first, last, tol_sq, keep):
    stack = [(first, last)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        dmax, idx = 0.0, -1
        for k in range(i + 1, j):
            d = _dist2_point_seg(xs[k], ys[k], xs[i], ys[i], xs[j], ys[j])
            if d > dmax:
                dmax, idx = d, k
        if dmax > tol_sq:
            keep[idx] = True
            stack.append((i, idx))
            stack.append((idx, j))


def simplificar_anillo(ring, tol):
    """Douglas-Peucker iterativo sobre un anillo [lon, lat]."""
    if len(ring) < 4:
        return ring
    cerrado = ring[0] == ring[-1]
    pts = ring[:-1] if cerrado else ring[:]
    n = len(pts)
    if n < 4:
        return ring
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    keep = [False] * n
    keep[0] = keep[n - 1] = True
    _dp_rec(xs, ys, 0, n - 1, tol * tol, keep)
    out = [pts[i] for i in range(n) if keep[i]]
    if cerrado and out:
        out.append(out[0])
    return out


def simplificar_geometria(geom, tol):
    tipo = geom.get("type")
    coords = geom.get("coordinates", [])
    if tipo == "Polygon":
        return {"type": "Polygon", "coordinates": [simplificar_anillo(r, tol) for r in coords]}
    if tipo == "MultiPolygon":
        polys = []
        for poly in coords:
            anillos = [simplificar_anillo(r, tol) for r in poly]
            anillos = [a for a in anillos if len(a) >= 4]
            if anillos:
                polys.append(anillos)
        return {"type": "MultiPolygon", "coordinates": polys}
    return geom


def leer_zip_csv(zip_name, miembro, encoding="latin-1"):
    """Itera las filas de un CSV dentro de un ZIP como diccionarios.
    Las cabeceras se normalizan a minusculas para que todas las fuentes
    (ITER 2010 en minusculas, ITER 2020 en mayusculas, DENUE mixto)
    se consulten igual."""
    with zipfile.ZipFile(DATA / zip_name) as zf:
        raw = zf.read(miembro)
    texto = io.TextIOWrapper(io.BytesIO(raw), encoding=encoding, errors="replace", newline="")
    reader = csv.reader(texto)
    try:
        cab = next(reader)
    except StopIteration:
        return
    cab = [h.strip().strip('"').lstrip("\ufeff").lower() for h in cab]
    for fila in reader:
        if len(fila) < len(cab):
            fila = fila + [""] * (len(cab) - len(fila))
        yield dict(zip(cab, fila))


def a_num(v, default=0.0):
    if v is None:
        return default
    v = str(v).strip().replace(",", "")
    if v in ("", "*", "N/D", "ND", "-", "ND/N/A"):
        return default
    try:
        return float(v)
    except ValueError:
        return default


# ------------------------------------------------------------- geojson INEGI
def cargar_geojson():
    CACHE.mkdir(parents=True, exist_ok=True)
    if not GEOJSON_CACHE.exists():
        print("  Descargando geometria municipal desde INEGI...")
        req = urllib.request.Request(GEOJSON_URL, headers={"User-Agent": "Tlaxcala-Urban-Growth/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r:
            GEOJSON_CACHE.write_bytes(r.read())
    gj = json.loads(GEOJSON_CACHE.read_text(encoding="utf-8"))
    feats = []
    for f in gj["features"]:
        p = f["properties"]
        feats.append(
            {
                "cve_mun": str(p["cve_mun"]).zfill(3),
                "cvegeo": p["cvegeo"],
                "nombre": p["nomgeo"],
                "pob_censo2020": int(p.get("pob_total") or 0),
                "viv_hab_censo2020": int(p.get("total_viviendas_habitadas") or 0),
                "geom": simplificar_geometria(f["geometry"], TOLERANCIA),
            }
        )
    feats.sort(key=lambda x: x["cve_mun"])
    return feats


# ------------------------------------------------------------------- ITER
def iter_municipios(zip_name, miembro, etiqueta):
    """Agrega ITER por municipio.

    Se usa la fila 'Total del Municipio' cuando existe (es la que usa el
    notebook); si un municipio no la trae, se suma el detalle de localidades.
    """
    suma = defaultdict(lambda: defaultdict(float))
    totales = {}
    for row in leer_zip_csv(zip_name, miembro):
        nom = (row.get("nom_mun") or "").strip()
        loc = (row.get("nom_loc") or "").strip()
        mun = (row.get("mun") or "").strip().zfill(3)
        if not nom or not mun or mun == "000":
            continue
        vals = {
            "POBTOT": a_num(row.get("pobtot")),
            "PRESOE15": a_num(row.get("presoe15")),
            "VIVPAR_HAB": a_num(row.get("vivpar_hab")),
            "VIVPAR_DES": a_num(row.get("vivpar_des")),
        }
        if normaliza(loc).startswith("TOTAL DEL MUNICIPIO"):
            totales[mun] = vals
            continue
        d = suma[mun]
        for k, v in vals.items():
            d[k] += v

    merged = {}
    fallback = []
    for mun in set(suma) | set(totales):
        if mun in totales:
            merged[mun] = dict(totales[mun])
        else:
            merged[mun] = dict(suma[mun])
            fallback.append(mun)
    print(f"  ITER {etiqueta}: {len(merged)} municipios ({len(totales)} con fila total, {len(fallback)} por suma de localidades)")
    return merged


# ------------------------------------------------------------------ DENUE
def denue_por_municipio(zip_name, miembro, etiqueta, geo_por_nombre):
    """Cuenta unidades economicas de alimentos y bebidas por municipio."""
    conteo = Counter()
    conteo_total = Counter()
    ocupacion = defaultdict(list)
    celdas = Counter()
    sin_match = Counter()

    # El DENUE 2010 usa "Nombre de la clase de actividad"; los posteriores,
    # "nombre_act".
    col_act = "nombre de la clase de actividad" if etiqueta == "2010" else "nombre_act"
    col_per = "personal ocupado (estrato)" if etiqueta == "2010" else "per_ocu"

    for row in leer_zip_csv(zip_name, miembro):
        nombre = (row.get("municipio") or "").strip()
        cve = (row.get("cve_mun") or "").strip().zfill(3)
        if not cve or cve == "000":
            clave = ALIAS_MUNICIPIO.get(normaliza(nombre), normaliza(nombre))
            cve = geo_por_nombre.get(clave, "")
        if not cve:
            sin_match[nombre] += 1
            continue
        conteo_total[cve] += 1
        if not coincide_actividad(row.get(col_act) or ""):
            continue
        conteo[cve] += 1
        per = a_num(row.get(col_per), 0)
        if per:
            ocupacion[cve].append(per)
        lat, lon = a_num(row.get("latitud"), 0), a_num(row.get("longitud"), 0)
        if lat and lon:
            celdas[(round(lat / CELDA), round(lon / CELDA))] += 1

    if sin_match:
        print(f"  [aviso] DENUE {etiqueta}: {sum(sin_match.values())} filas sin municipio reconocido")
        for n, c in sin_match.most_common(5):
            print(f"          {n!r} -> {c}")
    dens = [[round(k[0] * CELDA, 4), round(k[1] * CELDA, 4), v] for k, v in celdas.items()]
    print(
        f"  DENUE {etiqueta}: {sum(conteo.values())} alimentos y bebidas "
        f"en {len(conteo)} municipios | {len(dens)} celdas de densidad"
    )
    return dict(conteo), dict(conteo_total), dict(ocupacion), dens


# ------------------------------------------------------------------- main
def main():
    print("=" * 72)
    print("Construyendo dataset para el portal web")
    print("=" * 72)

    print("\n[1/5] Geometria municipal (INEGI)")
    feats = cargar_geojson()
    geo_por_nombre = {normaliza(f["nombre"]): f["cve_mun"] for f in feats}
    geo_por_cve = {f["cve_mun"]: f for f in feats}
    print(f"  {len(feats)} municipios, geometria simplificada (tol={TOLERANCIA})")

    print("\n[2/5] ITER 2010 / 2020")
    iter10 = iter_municipios("iter_29_2010_csv.zip", "iter_29_cpv2010/conjunto_de_datos/iter_29_cpv2010.csv", "2010")
    iter20 = iter_municipios(
        "iter_29_cpv2020_csv.zip", "iter_29_cpv2020/conjunto_de_datos/conjunto_de_datos_iter_29CSV20.csv", "2020"
    )

    print("\n[3/5] DENUE por año")
    denue = {}
    for zip_name, miembro, etiqueta in DENUE_ARCHIVOS:
        c, ct, oc, dens = denue_por_municipio(zip_name, miembro, etiqueta, geo_por_nombre)
        denue[etiqueta] = {"alim": c, "total": ct, "ocupacion": oc, "densidad": dens}

    print("\n[4/5] Consolidando por municipio")
    municipios = []
    for cve, geo in geo_por_cve.items():
        i10 = iter10.get(cve, {})
        i20 = iter20.get(cve, {})
        a10 = denue["2010"]["alim"].get(cve, 0)
        a25 = denue["2025"]["alim"].get(cve, 0)
        t10 = denue["2010"]["total"].get(cve, 0)
        t25 = denue["2025"]["total"].get(cve, 0)
        pob10 = i10.get("POBTOT", 0)
        pob20 = i20.get("POBTOT", 0)
        occ25 = denue["2025"]["ocupacion"].get(cve, [])
        occ10 = denue["2010"]["ocupacion"].get(cve, [])

        item = {
            "cve": cve,
            "nombre": geo["nombre"],
            "pob2010": int(pob10),
            "pob2020": int(pob20),
            "crec_pob_pct": round((pob20 - pob10) / pob10 * 100, 2) if pob10 else 0,
            "foraneos_pct": round(i20.get("PRESOE15", 0) / pob20 * 100, 2) if pob20 else 0,
            "foraneos_abs": int(i20.get("PRESOE15", 0)),
            "viv_deshab": int(i20.get("VIVPAR_DES", 0)),
            "viv_hab_2020": int(i20.get("VIVPAR_HAB", 0)),
            "alim2010": int(a10),
            "alim2025": int(a25),
            "crec_alim_pct": round((a25 - a10) / a10 * 100, 2) if a10 else 0,
            "total_unid2010": int(t10),
            "total_unid2025": int(t25),
            "crec_unid_pct": round((t25 - t10) / t10 * 100, 2) if t10 else 0,
            "alim_por_hab_2025": round(a25 / pob20 * 1000, 2) if pob20 else 0,
            "ocupacion_media_2025": round(sum(occ25) / len(occ25), 1) if occ25 else 0,
            "ocupacion_media_2010": round(sum(occ10) / len(occ10), 1) if occ10 else 0,
            "pob_censo2020": geo["pob_censo2020"],
            "viv_hab_censo2020": geo["viv_hab_censo2020"],
        }
        municipios.append(item)

    municipios.sort(key=lambda m: -m["crec_alim_pct"])
    total_alim10 = sum(m["alim2010"] for m in municipios)
    total_alim25 = sum(m["alim2025"] for m in municipios)
    print(
        f"  Total alimentos y bebidas: {total_alim10} (2010) -> {total_alim25} (2025) "
        f"(+{(total_alim25 / total_alim10 - 1) * 100:.1f}%)"
    )

    dif_censo = [m for m in municipios if abs(m["pob2020"] - m["pob_censo2020"]) > 0]
    print(f"  [control] ITER 2020 vs Censo 2020 (geojson INEGI): {len(dif_censo)} municipios con diferencia")
    for m in dif_censo[:5]:
        print(f"          {m['nombre']}: ITER={m['pob2020']} Censo={m['pob_censo2020']}")

    print("\n[5/5] Series temporales")
    etiquetas = [d[2] for d in DENUE_ARCHIVOS]
    series = {}
    for etiqueta in etiquetas:
        conteo = denue[etiqueta]["alim"]
        series[etiqueta] = [{"cve": cve, "n": conteo.get(cve, 0)} for cve in geo_por_cve]
    totales = [{"anio": e, "n": sum(denue[e]["alim"].values())} for e in etiquetas]

    dataset = {
        "meta": {
            "titulo": "Crecimiento Urbano de Tlaxcala",
            "subtitulo": "Gentrificacion comercial y dinamica demografica, 2010-2025",
            "fuentes": [
                "INEGI - ITER 2010 y 2020 (poblacion y vivienda)",
                "INEGI - DENUE 2010, 2023, 2024 y 2025 (unidades economicas)",
                "INEGI - Marco Geoestadistico via gaia.inegi.org.mx (geometria municipal)",
                "SHF - Indice de precios de la vivienda en Mexico, cierre 2025",
            ],
        },
        "shf": SHF,
        "totales": totales,
        "municipios": municipios,
        "series": series,
        "densidad": {"2010": denue["2010"]["densidad"], "2025": denue["2025"]["densidad"]},
        "geo": {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature", "properties": {"cve": f["cve_mun"], "nombre": f["nombre"]}, "geometry": f["geom"]}
                for f in feats
            ],
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(dataset, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"\nListo: {OUT.relative_to(ROOT)}  ({OUT.stat().st_size / 1024:.0f} KB)")

    # --- Autovalidacion contra las cifras publicadas en el notebook ---------
    print("\n" + "=" * 72)
    print("VALIDACION contra el notebook publicado")
    print("=" * 72)
    by_name = {m["nombre"].upper(): m for m in municipios}
    fallos = 0
    for nombre, exp in VALIDACION_PUBLICADA.items():
        m = by_name.get(nombre)
        if not m:
            print(f"  {nombre:13} NO ENCONTRADO")
            fallos += 1
            continue
        chk = {
            "alim2010": (m["alim2010"], exp["alim2010"]),
            "alim2025": (m["alim2025"], exp["alim2025"]),
            "crec_alim_pct": (round(m["crec_alim_pct"], 4), round(exp["pct"], 4)),
            "pob2010": (m["pob2010"], exp["pob2010"]),
            "pob2020": (m["pob2020"], exp["pob2020"]),
            "foraneos_pct": (round(m["foraneos_pct"], 4), round(exp["foraneo"], 4)),
        }
        bad = {k: v for k, v in chk.items() if abs(float(v[0]) - float(v[1])) > 0.01}
        if bad:
            fallos += 1
            print(f"  {nombre:13} DIFIERE")
            for k, v in bad.items():
                print(f"      {k}: calculado={v[0]}  notebook={v[1]}")
        else:
            print(f"  {nombre:13} OK")
    print("\n" + ("VALIDACION CORRECTA" if fallos == 0 else f"{fallos} MUNICIPIOS CON DISCREPANCIA"))

    print("\nTop 10 por crecimiento de alimentos y bebidas (2010-2025):")
    for m in municipios[:10]:
        print(f"  {m['nombre']:<40} {m['alim2010']:>5} -> {m['alim2025']:>5}  {m['crec_alim_pct']:>8.1f}%")

    return 0 if fallos == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
