<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import L from 'leaflet'
import { datos, fmtInt } from '../data/dataset.js'

const anio = ref('2025')
let mapa = null
let capa = null
const contenedor = ref(null)

const maxConteo = computed(() => {
  const d = datos.densidad[anio.value]
  return d.reduce((m, c) => Math.max(m, c[2]), 1)
})

function pintar() {
  if (!mapa) return
  if (capa) {
    capa.remove()
    capa = null
  }
  const max = maxConteo.value
  capa = L.layerGroup(
    datos.densidad[anio.value].map(([lat, lon, n]) =>
      L.circleMarker([lat, lon], {
        radius: 3 + Math.sqrt(n / max) * 22,
        color: 'rgba(180, 83, 9, 0.55)',
        weight: 0,
        fillColor: '#f59e0b',
        fillOpacity: 0.16 + Math.sqrt(n / max) * 0.5,
      }),
    ),
  ).addTo(mapa)
}

onMounted(() => {
  mapa = L.map(contenedor.value, {
    center: [19.32, -98.24],
    zoom: 9,
    minZoom: 8,
    maxZoom: 13,
    scrollWheelZoom: false,
  })
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap',
  }).addTo(mapa)
  pintar()
})

onBeforeUnmount(() => {
  if (mapa) {
    mapa.remove()
    mapa = null
  }
})

const total = computed(() => datos.densidad[anio.value].reduce((a, c) => a + c[2], 0))
</script>

<template>
  <div class="dens">
    <div class="dens__bar">
      <div class="controls">
        <button
          type="button"
          class="chip"
          :aria-pressed="anio === '2010'"
          @click="anio = '2010'; pintar()"
        >
          <span class="chip__dot" style="background: #9aa3b2"></span>
          2010
        </button>
        <button
          type="button"
          class="chip"
          :aria-pressed="anio === '2025'"
          @click="anio = '2025'; pintar()"
        >
          <span class="chip__dot" style="background: #f59e0b"></span>
          2025
        </button>
      </div>
      <p class="dens__total">
        <span class="num">{{ fmtInt(total) }}</span> establecimientos de alimentos y bebidas
        concentados en {{ fmtInt(datos.densidad[anio].length) }} celdas de ~550 m
      </p>
    </div>

    <div class="map-shell">
      <div ref="contenedor" class="map-canvas map-canvas--short"></div>
      <div class="map-legend">
        <p class="map-legend__title">Densidad</p>
        <div class="dens__ramp" aria-hidden="true">
          <span style="background: rgba(245, 158, 11, 0.16)"></span>
          <span style="background: rgba(245, 158, 11, 0.38)"></span>
          <span style="background: rgba(245, 158, 11, 0.66)"></span>
        </div>
        <div class="legend-ramp__ends">
          <span>baja</span>
          <span>alta</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dens__bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 18px;
}

.dens__total {
  font-size: 13px;
  color: var(--muted);
}

.dens__total .num {
  color: var(--ink);
  font-weight: 500;
}

.map-canvas--short {
  height: 440px;
}

@media (min-width: 768px) {
  .map-canvas--short {
    height: 500px;
  }
}

.dens__ramp {
  display: flex;
  border-radius: 4px;
  overflow: hidden;
}

.dens__ramp span {
  width: 30px;
  height: 9px;
  display: block;
}
</style>
