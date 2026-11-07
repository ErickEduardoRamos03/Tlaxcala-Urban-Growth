<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import L from 'leaflet'
import { datos, porCve, fmtInt, fmt2, fmtPct, colorPorCortes, RAMP } from '../data/dataset.js'

// Los cortes se eligieron por cuantiles sobre la distribucion real de los 60
// municipios, de modo que cada tramo tenga una cantidad comparable de casos
// y el mapa discrimine de verdad.
const METRICAS = [
  {
    key: 'crec_alim_pct',
    etiqueta: 'Crecimiento comercial',
    desc: 'Variacion % de alimentos y bebidas, 2010-2025',
    breaks: [0, 30, 50, 70, 95, 130, Infinity],
    formato: (v) => fmtPct(v),
    leyenda: ['<30%', '30%', '50%', '70%', '95%', '130%+'],
  },
  {
    key: 'alim2025',
    etiqueta: 'Establecimientos 2025',
    desc: 'Total de alimentos y bebidas por municipio',
    breaks: [0, 100, 200, 350, 600, 1200, Infinity],
    formato: (v) => fmtInt(v),
    leyenda: ['0', '100', '200', '350', '600', '1200+'],
  },
  {
    key: 'alim_por_hab_2025',
    etiqueta: 'Densidad comercial',
    desc: 'Establecimientos por cada mil habitantes',
    breaks: [0, 12, 16, 19, 22, 25, Infinity],
    formato: (v) => fmt2(v),
    leyenda: ['0', '12', '16', '19', '22', '25+'],
  },
  {
    key: 'foraneos_pct',
    etiqueta: 'Poblacion foranea',
    desc: 'Porcentaje de poblacion procedente de otra entidad, 2020',
    breaks: [0, 1.5, 2, 2.5, 3.5, 4.5, Infinity],
    formato: (v) => fmt2(v) + '%',
    leyenda: ['0%', '1.5%', '2%', '2.5%', '3.5%', '4.5%+'],
  },
  {
    key: 'crec_pob_pct',
    etiqueta: 'Crecimiento poblacional',
    desc: 'Variacion % de poblacion, 2010-2020',
    breaks: [0, 8, 11, 14, 17, 22, Infinity],
    formato: (v) => fmtPct(v),
    leyenda: ['<8%', '8%', '11%', '14%', '17%', '22%+'],
  },
]

const metricas = METRICAS
const metricaKey = ref('crec_alim_pct')
const metrica = computed(() => metricas.find((m) => m.key === metricaKey.value))
const seleccionado = ref(null)

let mapa = null
let capaGeo = null
const contenedor = ref(null)

function colorDe(muni) {
  return colorPorCortes(muni[metrica.value.key], metrica.value.breaks)
}

function estilo(muni) {
  const sel = seleccionado.value?.cve === muni.cve
  return {
    fillColor: colorDe(muni),
    fillOpacity: sel ? 0.95 : 0.78,
    color: sel ? '#14171e' : '#ffffff',
    weight: sel ? 2.4 : 0.9,
  }
}

/** Leaflet no acepta una funcion en setStyle: hay que iterar las capas. */
function pintar() {
  if (!capaGeo) return
  capaGeo.eachLayer((layer) => {
    const muni = porCve[layer.feature.properties.cve]
    layer.setStyle(estilo(muni))
    layer.setTooltipContent(
      `<strong>${muni.nombre}</strong><br/>${metrica.value.etiqueta}: ${metrica.value.formato(muni[metrica.value.key])}`,
    )
  })
}

function seleccionar(muni) {
  seleccionado.value = seleccionado.value?.cve === muni.cve ? null : muni
  pintar()
}

onMounted(() => {
  mapa = L.map(contenedor.value, {
    center: [19.32, -98.24],
    zoom: 9,
    minZoom: 8,
    maxZoom: 13,
    scrollWheelZoom: false,
    zoomControl: true,
    attributionControl: true,
  })
  mapa.on('click', () => {
    if (seleccionado.value) {
      seleccionado.value = null
      pintar()
    }
  })

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap',
  }).addTo(mapa)

  capaGeo = L.geoJSON(datos.geo, {
    style: (feature) => estilo(porCve[feature.properties.cve]),
    onEachFeature(feature, layer) {
      const muni = porCve[feature.properties.cve]
      layer.bindTooltip(
        `<strong>${muni.nombre}</strong><br/>${metrica.value.etiqueta}: ${metrica.value.formato(muni[metrica.value.key])}`,
        { sticky: true, direction: 'top', className: 'map-tip' },
      )
      layer.on('mouseover', () => layer.setStyle({ weight: 2.2, color: '#14171e', fillOpacity: 0.92 }))
      layer.on('mouseout', () => layer.setStyle(estilo(muni)))
      layer.on('click', (ev) => {
        L.DomEvent.stop(ev)
        seleccionar(muni)
      })
    },
  }).addTo(mapa)

  mapa.fitBounds(capaGeo.getBounds(), { padding: [18, 18] })
  pintar()
})

onBeforeUnmount(() => {
  if (mapa) {
    mapa.remove()
    mapa = null
  }
})

const detalle = computed(() => {
  const m = seleccionado.value
  if (!m) return null
  return {
    nombre: m.nombre,
    alim2010: fmtInt(m.alim2010),
    alim2025: fmtInt(m.alim2025),
    crec: fmtPct(m.crec_alim_pct),
    pob2020: fmtInt(m.pob2020),
    pob2010: fmtInt(m.pob2010),
    crecPob: fmtPct(m.crec_pob_pct),
    foraneos: fmt2(m.foraneos_pct) + '%',
    densidad: fmt2(m.alim_por_hab_2025),
    vivDeshab: fmtInt(m.viv_deshab),
  }
})
</script>

<template>
  <div class="chor">
    <div class="chor__controls">
      <div class="controls">
        <button
          v-for="m in metricas"
          :key="m.key"
          type="button"
          class="chip"
          :aria-pressed="metricaKey === m.key"
          @click="metricaKey = m.key; pintar()"
        >
          {{ m.etiqueta }}
        </button>
      </div>
      <p class="chor__desc">{{ metrica.desc }}</p>
    </div>

    <div class="chor__body">
      <div class="map-shell">
        <div ref="contenedor" class="map-canvas"></div>
        <div class="map-legend">
          <p class="map-legend__title">{{ metrica.etiqueta }}</p>
          <div class="legend-ramp">
            <div class="legend-ramp__swatches">
              <i v-for="(c, i) in RAMP" :key="i" :style="{ background: c }"></i>
            </div>
          </div>
          <div class="legend-ramp__ends">
            <span>{{ metrica.leyenda[0] }}</span>
            <span>{{ metrica.leyenda[metrica.leyenda.length - 1] }}</span>
          </div>
        </div>
      </div>

      <aside class="chor__panel card card--pad">
        <template v-if="detalle">
          <p class="eyebrow">Municipio seleccionado</p>
          <h3 class="chor__name">{{ detalle.nombre }}</h3>

          <div class="chor__big">
            <p class="chor__big-value num">{{ detalle.crec }}</p>
            <p class="chor__big-cap">crecimiento en alimentos y bebidas</p>
          </div>

          <div class="chor__pair">
            <div>
              <p class="chor__pair-value num">{{ detalle.alim2010 }}</p>
              <p class="chor__pair-cap">establecimientos 2010</p>
            </div>
            <svg class="chor__arrow" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M5 12h14" /><path d="m12 5 7 7-7 7" />
            </svg>
            <div>
              <p class="chor__pair-value num">{{ detalle.alim2025 }}</p>
              <p class="chor__pair-cap">establecimientos 2025</p>
            </div>
          </div>

          <dl class="kv">
            <dt>Poblacion 2020</dt>
            <dd class="num">{{ detalle.pob2020 }}</dd>
            <dt>Crecimiento pob.</dt>
            <dd class="num">{{ detalle.crecPob }}</dd>
            <dt>Poblacion foranea</dt>
            <dd class="num">{{ detalle.foraneos }}</dd>
            <dt>Establec. x mil hab.</dt>
            <dd class="num">{{ detalle.densidad }}</dd>
            <dt>Viviendas deshabitadas</dt>
            <dd class="num">{{ detalle.vivDeshab }}</dd>
          </dl>

          <button type="button" class="chor__close" @click="seleccionado = null; pintar()">
            Cerrar detalle
          </button>
        </template>

        <template v-else>
          <p class="eyebrow">Como leer el mapa</p>
          <h3 class="chor__name">Selecciona un municipio</h3>
          <p class="card-sub chor__hint">
            Cada poligono es un municipio de Tlaxcala. Pasa el cursor para ver el valor y haz clic
            para abrir su ficha completa con los datos demograficos y de vivienda.
          </p>
          <ul class="chor__tips">
            <li>
              <span class="chor__tip-dot" :style="{ background: RAMP[0] }"></span>
              Menor crecimiento del estado
            </li>
            <li>
              <span class="chor__tip-dot" :style="{ background: RAMP[3] }"></span>
              Crecimiento moderado
            </li>
            <li>
              <span class="chor__tip-dot" :style="{ background: RAMP[5] }"></span>
              Crecimiento superior al 130%
            </li>
          </ul>
        </template>
      </aside>
    </div>
  </div>
</template>

<style scoped>
.chor__controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 18px;
}

.chor__desc {
  font-size: 13px;
  color: var(--muted);
}

.chor__body {
  display: grid;
  gap: 18px;
}

@media (min-width: 1000px) {
  .chor__body {
    grid-template-columns: minmax(0, 1fr) 320px;
    align-items: start;
  }
}

.chor__panel {
  position: sticky;
  top: 84px;
}

@media (max-width: 999px) {
  .chor__panel {
    position: static;
  }
}

.chor__name {
  margin-top: 10px;
  font-size: 21px;
  line-height: 1.2;
}

.chor__hint {
  margin-top: 10px;
}

.chor__big {
  margin-top: 20px;
  padding: 16px;
  border-radius: 12px;
  background: var(--accent-soft);
  border: 1px solid var(--accent-line);
}

.chor__big-value {
  font-size: 32px;
  line-height: 1;
  color: var(--accent-700);
}

.chor__big-cap {
  margin-top: 6px;
  font-size: 12.5px;
  color: var(--ink-2);
}

.chor__pair {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 12px;
  align-items: center;
  margin: 20px 0;
  padding: 16px 0;
  border-top: 1px solid var(--line-soft);
  border-bottom: 1px solid var(--line-soft);
}

.chor__pair-value {
  font-size: 19px;
  line-height: 1.15;
}

.chor__pair-cap {
  margin-top: 4px;
  font-size: 11.5px;
  color: var(--muted);
}

.chor__arrow {
  color: var(--accent-600);
}

.kv {
  display: grid;
  grid-template-columns: 1fr auto;
  row-gap: 9px;
  column-gap: 14px;
  margin: 0;
}

.kv dt {
  font-size: 12.5px;
  color: var(--muted);
  border-bottom: 1px dashed var(--line);
  padding-bottom: 8px;
}

.kv dd {
  margin: 0;
  font-size: 13px;
  text-align: right;
  border-bottom: 1px dashed var(--line);
  padding-bottom: 8px;
}

.chor__close {
  margin-top: 20px;
  width: 100%;
  padding: 9px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: var(--surface);
  color: var(--ink-2);
  font-size: 13px;
  font-weight: 500;
  transition: all 0.16s ease;
}

.chor__close:hover {
  border-color: var(--accent-line);
  color: var(--ink);
}

.chor__tips {
  margin: 18px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 9px;
  font-size: 12.5px;
  color: var(--ink-2);
}

.chor__tips li {
  display: flex;
  align-items: center;
  gap: 9px;
}

.chor__tip-dot {
  width: 12px;
  height: 12px;
  border-radius: 3px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  flex-shrink: 0;
}
</style>
