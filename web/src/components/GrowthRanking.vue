<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import {
  Chart,
  BarController,
  BarElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
} from 'chart.js'
import { datos } from '../data/dataset.js'

Chart.register(BarController, BarElement, PointElement, CategoryScale, LinearScale, Tooltip)

const modo = ref('pct')
const lienzo = ref(null)
let grafica = null

const TOP = 15

const filas = computed(() => {
  const arr = [...datos.municipios]
  if (modo.value === 'pct') {
    return arr.sort((a, b) => b.crec_alim_pct - a.crec_alim_pct).slice(0, TOP)
  }
  return arr
    .map((m) => ({ ...m, delta: m.alim2025 - m.alim2010 }))
    .sort((a, b) => b.delta - a.delta)
    .slice(0, TOP)
})

function construir() {
  if (!lienzo.value) return
  if (grafica) grafica.destroy()

  const etiquetas = filas.value.map((m) => m.nombre)
  const valores = filas.value.map((m) =>
    modo.value === 'pct' ? m.crec_alim_pct : m.alim2025 - m.alim2010,
  )

  grafica = new Chart(lienzo.value, {
    type: 'bar',
    data: {
      labels: etiquetas,
      datasets: [
        {
          data: valores,
          backgroundColor: valores.map((v) =>
            v >= 0 ? 'rgba(245, 158, 11, 0.82)' : 'rgba(148, 163, 184, 0.75)',
          ),
          borderRadius: 5,
          borderSkipped: false,
          maxBarThickness: 22,
        },
      ],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 650, easing: 'easeOutQuart' },
      layout: { padding: { right: 18 } },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#14171e',
          padding: 12,
          cornerRadius: 10,
          titleFont: { family: 'Outfit', size: 13, weight: '600' },
          bodyFont: { family: 'JetBrains Mono', size: 12 },
          displayColors: false,
          callbacks: {
            label(ctx) {
              const m = filas.value[ctx.dataIndex]
              if (modo.value === 'pct') {
                return ` +${ctx.parsed.x.toFixed(1)}%   (${m.alim2010} → ${m.alim2025})`
              }
              return ` +${ctx.parsed.x} establecimientos   (${m.alim2010} → ${m.alim2025})`
            },
          },
        },
      },
      scales: {
        x: {
          grid: { color: 'rgba(0,0,0,0.045)', drawTicks: false },
          border: { display: false },
          ticks: {
            font: { family: 'JetBrains Mono', size: 11 },
            color: '#8b8981',
            callback: (v) => (modo.value === 'pct' ? `${v}%` : v),
          },
        },
        y: {
          grid: { display: false },
          border: { display: false },
          ticks: {
            font: { family: 'Outfit', size: 12, weight: '500' },
            color: '#3a4256',
            crossAlign: 'far',
          },
        },
      },
    },
  })
}

onMounted(construir)
watch(modo, construir)
onBeforeUnmount(() => {
  if (grafica) grafica.destroy()
})
</script>

<template>
  <div class="rank">
    <div class="rank__head">
      <div class="controls">
        <button
          type="button"
          class="chip"
          :aria-pressed="modo === 'pct'"
          @click="modo = 'pct'"
        >
          Crecimiento %
        </button>
        <button
          type="button"
          class="chip"
          :aria-pressed="modo === 'abs'"
          @click="modo = 'abs'"
        >
          Aumento absoluto
        </button>
      </div>
      <p class="rank__note">
        Top {{ TOP }} de 60 municipios ·
        {{ modo === 'pct' ? 'variación porcentual 2010-2025' : 'establecimientos ganados 2010-2025' }}
      </p>
    </div>

    <div class="chart-frame chart-frame--tall" style="height: 620px">
      <canvas ref="lienzo"></canvas>
    </div>
  </div>
</template>

<style scoped>
.rank__head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 22px;
}

.rank__note {
  font-size: 13px;
  color: var(--muted);
}

@media (max-width: 640px) {
  .chart-frame--tall {
    height: 560px;
  }
}
</style>
