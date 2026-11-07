# -*- coding: utf-8 -*-
"""Valida la ejecucion del notebook: errores, cifras clave y graficas generadas."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent
NB = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "Analisis_Crecimiento_Urbano_Tlaxcala.ipynb"
if not NB.is_absolute():
    NB = ROOT / NB

nb = json.loads(NB.read_text(encoding="utf-8"))
cells = nb["cells"]

# --- 1. Errores -------------------------------------------------------------
errores = []
for i, c in enumerate(cells):
    for o in c.get("outputs", []):
        if o.get("output_type") == "error":
            errores.append((i, o.get("ename"), o.get("evalue")))
print("== ERRORES ==")
print("ninguno" if not errores else errores)

# --- 2. Graficas embebidas --------------------------------------------------
imgs = sum(
    1
    for c in cells
    for o in c.get("outputs", [])
    if "image/png" in o.get("data", {})
)
print(f"\n== GRAFICAS ==\nimagenes embebidas en el notebook: {imgs}")

out_dir = ROOT / "output"
pngs = sorted(out_dir.glob("*.png")) if out_dir.is_dir() else []
print(f"PNGs en output/: {len(pngs)}")
for p in pngs:
    print(f"  {p.name}  ({p.stat().st_size / 1024:.0f} KB)")

# --- 3. Cifras clave --------------------------------------------------------
esperado = {
    "HUAMANTLA": (1079, 1693, 56.904541),
    "TLAXCALA": (1437, 2127, 48.016701),
    "CHIAUTEMPAN": (1222, 1727, 41.325696),
    "APIZACO": (1523, 1882, 23.571898),
}


def textos(i):
    out = []
    for o in cells[i].get("outputs", []):
        if o.get("output_type") == "stream":
            out.append("".join(o.get("text", [])))
        elif o.get("output_type") == "execute_result":
            d = o.get("data", {})
            if "text/plain" in d:
                out.append("".join(d["text/plain"]))
    return "\n".join(out)


print("\n== TABLA DENUE (celda 18) ==")
t18 = textos(18)
print(t18)

print("\n== COMPARACION CONTRA VALORES PUBLICADOS ==")
ok = True
for mun, (n10, n25, pct) in esperado.items():
    # se busca la linea del municipio en la salida de texto
    lineas = [ln for ln in t18.splitlines() if mun in ln]
    if not lineas:
        print(f"  {mun}: NO ENCONTRADO")
        ok = False
        continue
    nums = lineas[0].split()
    try:
        g10, g25, gpct = int(nums[1]), int(nums[2]), float(nums[3])
    except Exception:
        print(f"  {mun}: no parseable -> {lineas[0]!r}")
        ok = False
        continue
    coincide = (g10 == n10 and g25 == n25 and abs(gpct - pct) < 1e-4)
    ok = ok and coincide
    print(f"  {mun:12} 2010={g10} 2025={g25} pct={gpct:.6f}  ->  {'OK' if coincide else 'DIFIERE'}")

print("\n== ITER 2020: % foraneos (celda 13) ==")
print(textos(13))
print("\n== CRECIMIENTO POBLACIONAL 2010-2020 (celda 15) ==")
print(textos(15))

print("\nRESULTADO:", "TODAS LAS CIFRAS COINCIDEN" if ok and not errores else "REVISAR")
sys.exit(0 if (ok and not errores and imgs == 4 and len(pngs) == 4) else 1)
