<script setup>
import { datos } from '../data/dataset.js'

const PASOS = [
  {
    n: '01',
    t: 'Extraccion',
    d: 'Los archivos .zip de INEGI dentro de data/ se descomprimen con zipfile. El repositorio ya incluye los datos crudos, asi que el portal se reconstruye sin red.',
  },
  {
    n: '02',
    t: 'Agregacion',
    d: 'El ITER 2010 y 2020 aporta poblacion, poblacion foranea (PRESOE15) y vivienda por municipio. Se usa la fila "Total del Municipio", que es la que emplea el cuaderno original.',
  },
  {
    n: '03',
    t: 'Actividad economica',
    d: 'El DENUE clasifica cada establecimiento por actividad. Se filtran los giros de alimentos y bebidas con las mismas palabras clave del cuaderno, sin normalizar acentos: hacerlo contaria como comida negocios de copiado y fabricas textiles.',
  },
  {
    n: '04',
    t: 'Geometria',
    d: 'El Marco Geoestadistico del INEGI aporta los poligonos de los 60 municipios. Se simplifican con Douglas-Peucker para reducir el peso del mapa sin perder la silueta.',
  },
  {
    n: '05',
    t: 'Validacion',
    d: 'El pipeline comprueba que las cifras de los cuatro municipios centrales reproducen exactamente las publicadas en el cuaderno. Si divergen, el build falla.',
  },
]
</script>

<template>
  <div class="met">
    <div class="met__grid">
      <ol class="met__steps">
        <li v-for="p in PASOS" :key="p.n" class="met__step">
          <span class="met__step-n num">{{ p.n }}</span>
          <div>
            <h3 class="met__step-t">{{ p.t }}</h3>
            <p class="met__step-d">{{ p.d }}</p>
          </div>
        </li>
      </ol>

      <aside class="met__side">
        <div class="card card--pad">
          <h3 class="card-title">Fuentes</h3>
          <ul class="met__list">
            <li v-for="f in datos.meta.fuentes" :key="f">{{ f }}</li>
          </ul>
        </div>

        <div class="card card--pad met__caveat">
          <h3 class="card-title">Por que solo 2010 y 2025</h3>
          <p class="card-sub">
            El repositorio incluye snapshots intermedios del DENUE (nov-2023, may-2024 y
            nov-2024), pero no son comparables entre si: al publicar cada edicion, INEGI
            reescribe masivamente el campo <code>fecha_alta</code>. Entre may-2024 y
            nov-2024 el directorio paso de 83,021 a 97,544 registros, y unas 14,800 altas
            de 2019 fueron reestampadas como 2024. Graficar esa serie produciria un
            crecimiento artificial.
          </p>
          <p class="card-sub">
            El portal compara por tanto los dos cortes que si son solidos: los extremos
            2010 y 2025, con la metodologia del cuaderno original.
          </p>
        </div>

        <div class="card card--pad">
          <h3 class="card-title">Limites</h3>
          <ul class="met__list met__list--plain">
            <li>El DENUE mide establecimientos, no empleo formal ni facturacion.</li>
            <li>El indice SHF solo esta disponible a nivel estatal y nacional.</li>
            <li>El ITER llega hasta 2020; el censo 2025 no estaba disponible al construir este portal.</li>
            <li>La poblacion foranea se mide por residencia declarada en 2015, registrada en el censo de 2020.</li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.met__grid {
  display: grid;
  gap: 32px;
  grid-template-columns: repeat(12, minmax(0, 1fr));
}

.met__steps {
  grid-column: span 12;
  margin: 0;
  padding: 0;
  list-style: none;
  position: relative;
}

@media (min-width: 940px) {
  .met__steps {
    grid-column: span 7;
  }
  .met__side {
    grid-column: span 5;
  }
}

.met__step {
  position: relative;
  padding: 0 0 26px 44px;
}

.met__step::before {
  content: '';
  position: absolute;
  left: 11px;
  top: 22px;
  bottom: -4px;
  width: 2px;
  background: linear-gradient(180deg, var(--accent-line), rgba(245, 158, 11, 0.08));
}

.met__step:last-child {
  padding-bottom: 0;
}

.met__step:last-child::before {
  display: none;
}

.met__step-n {
  position: absolute;
  left: 0;
  top: 0;
  display: grid;
  place-items: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid var(--accent);
  background: var(--bg);
  color: var(--accent-700);
  font-size: 10.5px;
  font-weight: 500;
}

.met__step-t {
  font-size: 16px;
}

.met__step-d {
  margin-top: 7px;
  font-size: 14px;
  font-weight: 300;
  line-height: 1.65;
  color: var(--ink-2);
}

.met__side {
  grid-column: span 12;
  display: grid;
  gap: 16px;
  align-content: start;
}

.met__list {
  margin: 14px 0 0;
  padding-left: 18px;
  display: grid;
  gap: 8px;
  font-size: 13.5px;
  line-height: 1.55;
  color: var(--ink-2);
}

.met__list--plain {
  list-style: none;
  padding-left: 0;
}

.met__list--plain li {
  position: relative;
  padding-left: 16px;
}

.met__list--plain li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 9px;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--accent);
}

.met__caveat code {
  font-family: var(--mono);
  font-size: 12px;
  background: var(--surface-2);
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 1px 5px;
}
</style>
