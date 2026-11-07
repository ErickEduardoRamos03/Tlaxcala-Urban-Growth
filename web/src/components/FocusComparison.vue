<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import {
  Chart,
  BarController,
  BarElement,
  LineController,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js'
import { FOCUS, fmtInt, fmtPct } from '../data/dataset.js'

Chart.register(
  BarController,
  BarElement,
  LineController,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
)

const lienzoComercial = ref(null)
const lienzoDemo = ref(null)
let gComercial = null
let gDemo = null

const etiquetas = computed(() => FOCUS.map((m) => m.nombre.toUpperCase()))

function construirComercial() {
  if (!lienzoComercial.value) return
  if (gComercial) gComercial.destroy()

  const alineado = [...FOCUS].sort((a, b) => b.crec_alim_pct - a.crec_alim_pct)

  gComercial = new Chart(lienzoComercial.value, {
    type: 'bar',
    data: {
      labels: alineado.map((m) => m.nombre.toUpperCase()),
      datasets: [
        {
          label: '2010',
          data: alineado.map((m) => m.alim2010),
          backgroundColor: 'rgba(154, 163, 178, 0.55)',
          borderRadius: 5,
          borderSkipped: false,
          maxBarThickness: 34,
        },
        {
          label: '2025',
          data: alineado.map((m) => m.alim2025),
          backgroundColor: 'rgba(245, 158, 11, 0.85)',
          borderRadius: 5,
          borderSkipped: false,
          maxBarThickness: 34,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 650, easing: 'easeOutQuart' },
      plugins: {
        legend: {
          position: 'top',
          align: 'end',
          labels: {
            boxWidth: 10,
            boxHeight: 10,
            borderRadius: 3,
            font: { family: 'Outfit', size: 12.5, weight: '500' },
            color: '#3a4256',
          },
        },
        tooltip: {
          backgroundColor: '#14171e',
          padding: 12,
          cornerRadius: 10,
          titleFont: { family: 'Outfit', size: 13, weight: '600' },
          bodyFont: { family: 'JetBrains Mono', size: 12 },
          displayColors: true,
          boxWidth: 10,
          boxHeight: 10,
          callbacks: {
            afterBody(ctx) {
              const m = alineado[ctx[0].dataIndex]
              return `crecimiento: ${fmtPct(m.crec_alim_pct)}`
            },
          },
        },
      },
      scales: {
        x: {
          grid: { display: false },
          border: { display: false },
          ticks: { font: { family: 'Outfit', size: 12, weight: '500' }, color: '#3a4256' },
        },
        y: {
          grid: { color: 'rgba(0,0,0,0.045)', drawTicks: false },
          border: { display: false },
          title: { display: true, text: 'Establecimientos', font: { family: 'Outfit', size: 12 } },
          ticks: { font: { family: 'JetBrains Mono', size: 11 }, color: '#8b8981' },
        },
      },
    },
  })
}

function construirDemo() {
  if (!lienzoDemo.value) return
  if (gDemo) gDemo.destroy()

  const alineado = [...FOCUS].sort((a, b) => b.crec_pob_pct - a.crec_pob_pct)

  gDemo = new Chart(lienzoDemo.value, {
    data: {
      labels: alineado.map((m) => m.nombre.toUpperCase()),
      datasets: [
        {
          type: 'bar',
          label: 'Crecimiento poblacional %',
          data: alineado.map((m) => m.crec_pob_pct),
          backgroundColor: 'rgba(245, 158, 11, 0.42)',
          borderRadius: 5,
          borderSkipped: false,
          maxBarThickness: 38,
          order: 2,
          yAxisID: 'y',
        },
        {
          type: 'line',
          label: 'Poblacion foranea %',
          data: alineado.map((m) => m.foraneos_pct),
          borderColor: '#b91c1c',
          backgroundColor: '#b91c1c',
          borderWidth: 2.4,
          pointRadius: 5,
          pointStyle: 'rectRot',
          tension: 0.3,
          order: 1,
          yAxisID: 'y1',
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 650, easing: 'easeOutQuart' },
      plugins: {
        legend: {
          position: 'top',
          align: 'end',
          labels: {
            boxWidth: 10,
            boxHeight: 10,
            borderRadius: 3,
            font: { family: 'Outfit', size: 12.5, weight: '500' },
            color: '#3a4256',
          },
        },
        tooltip: {
          backgroundColor: '#14171e',
          padding: 12,
          cornerRadius: 10,
          titleFont: { family: 'Outfit', size: 13, weight: '600' },
          bodyFont: { family: 'JetBrains Mono', size: 12 },
          boxWidth: 10,
          boxHeight: 10,
        },
      },
      scales: {
        x: {
          grid: { display: false },
          border: { display: false },
          ticks: { font: { family: 'Outfit', size: 12, weight: '500' }, color: '#3a4256' },
        },
        y: {
          position: 'left',
          grid: { color: 'rgba(0,0,0,0.045)', drawTicks: false },
          border: { display: false },
          title: { display: true, text: '% crecimiento poblacional', font: { family: 'Outfit', size: 11.5 } },
          ticks: { font: { family: 'JetBrains Mono', size: 11 }, color: '#8b8981' },
        },
        y1: {
          position: 'right',
          grid: { display: false },
          border: { display: false },
          title: { display: true, text: '% foraneos', font: { family: 'Outfit', size: 11.5 } },
          ticks: { font: { family: 'JetBrains Mono', size: 11 }, color: '#b91c1c' },
        },
      },
    },
  })
}

onMounted(() => {
  construirComercial()
  construirDemo()
})

onBeforeUnmount(() => {
  if (gComercial) gComercial.destroy()
  if (gDemo) gDemo.destroy()
})
</script>

<template>
  <div class="focus">
    <article class="card card--pad">
      <p class="eyebrow">Los cuatro municipios del analisis original</p>
      <h3 class="card-title focus__title">Evolucion comercial 2010 vs 2025</h3>
      <p class="card-sub">
        Alimentos y bebidas por municipio, con el crecimiento porcentual que
        destaca la publicacion original.
      </p>
      <div class="chart-frame" style="height: 360px; margin-top: 20px">
        <canvas ref="lienzoComercial"></canvas>
      </div>
      <div class="focus__stats">
        <div v-for="m in FOCUS" :key="m.cve" class="focus__stat">
          <span class="focus__stat-name">{{ m.nombre }}</span>
          <span class="focus__stat-val num">{{ fmtPct(m.crec_alim_pct) }}</span>
        </div>
      </div>
    </article>

    <article class="card card--pad">
      <p class="eyebrow">Demografia</p>
      <h3 class="card-title focus__title">Crecimiento vs. poblacion foranea</h3>
      <p class="card-sub">
        Crecimiento poblacional 2010-2020 frente al porcentaje de poblacion que en 2020
        residia en otra entidad. Donde la linea sube mas que las barras, el cambio es
        de composicion, no solo de tamano.
      </p>
      <div class="chart-frame" style="height: 360px; margin-top: 20px">
        <canvas ref="lienzoDemo"></canvas>
      </div>
    </article>
  </div>
</template>

<style scoped>
.focus {
  display: grid;
  gap: 18px;
  grid-template-columns: repeat(12, minmax(0, 1fr));
}

.focus > * {
  grid-column: span 12;
}

@media (min-width: 1000px) {
  .focus > *:first-child {
    grid-column: span 7;
  }
  .focus > *:last-child {
    grid-column: span 5;
  }
}

.focus__title {
  margin-top: 10px;
  font-size: 18px;
}

.focus__stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--line-soft);
}

.focus__stat {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 10px;
}

.focus__stat-name {
  font-size: 12.5px;
  color: var(--muted);
}

.focus__stat-val {
  font-size: 14px;
  color: var(--accent-700);
}
</style>
