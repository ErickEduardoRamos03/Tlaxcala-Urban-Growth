<script setup>
import { computed } from 'vue'
import { fmtInt, fmt1, fmtPct, totalAlim2010, totalAlim2025, crecTotalPct, topCrecimiento } from '../data/dataset.js'

const estadisticas = computed(() => [
  {
    valor: fmtPct(crecTotalPct),
    etiqueta: 'establecimientos de alimentos y bebidas',
    pie: `${fmtInt(totalAlim2010)} en 2010 · ${fmtInt(totalAlim2025)} en 2025`,
    destacado: true,
  },
  {
    valor: '+12.0%',
    etiqueta: 'precio de vivienda en Tlaxcala',
    pie: 'frente a +8.7% del promedio nacional (SHF)',
  },
  {
    valor: '4.57%',
    etiqueta: 'de la poblacion de Tlaxcala es foranea',
    pie: 'el valor mas alto de los cuatro municipios analizados',
  },
  {
    valor: fmt1(topCrecimiento[0].crec_alim_pct) + '%',
    etiqueta: 'crecimiento maximo en un municipio',
    pie: `${topCrecimiento[0].nombre}, de ${fmtInt(topCrecimiento[0].alim2010)} a ${fmtInt(topCrecimiento[0].alim2025)}`,
  },
])
</script>

<template>
  <section id="inicio" class="hero">
    <div class="hero__glow" aria-hidden="true"></div>
    <div class="shell">
      <div class="hero__grid">
        <div class="hero__main">
          <p class="eyebrow">INEGI · ITER + DENUE · 2010 – 2025</p>
          <h1 class="hero__title">
            La gentrificación comercial de Tlaxcala
            <span class="hero__title-accent">ya no vive en el centro</span>
          </h1>
          <p class="hero__lead">
            En quince años los negocios de alimentos y bebidas del estado crecieron
            <strong>{{ fmtPct(crecTotalPct) }}</strong>. Pero el avance porcentual más alto ya no está en la
            capital: lo lideran la corona periurbana, mientras el centro compensa con volumen.
          </p>
          <div class="hero__actions">
            <a href="#mapa" class="btn btn--primary">
              Ver el mapa
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 12h14" />
                <path d="m12 5 7 7-7 7" />
              </svg>
            </a>
            <a href="#metodologia" class="btn btn--ghost">Cómo se calculó</a>
          </div>
        </div>

        <aside class="hero__panel card">
          <p class="hero__panel-label">El dato que resume el hallazgo</p>
          <div class="hero__panel-row">
            <div>
              <p class="hero__panel-value num">{{ fmtPct(crecTotalPct) }}</p>
              <p class="hero__panel-cap">en alimentos y bebidas</p>
            </div>
            <div class="hero__panel-split" aria-hidden="true">
              <span>2010</span>
              <span>2025</span>
            </div>
          </div>
          <div class="hero__bars">
            <div class="hero__bar">
              <span class="hero__bar-label">2010</span>
              <div class="hero__bar-track">
                <div class="hero__bar-fill hero__bar-fill--past" :style="{ width: '100%' }"></div>
              </div>
              <span class="hero__bar-val num">{{ fmtInt(totalAlim2010) }}</span>
            </div>
            <div class="hero__bar">
              <span class="hero__bar-label">2025</span>
              <div class="hero__bar-track">
                <div class="hero__bar-fill" :style="{ width: '100%' }"></div>
              </div>
              <span class="hero__bar-val num">{{ fmtInt(totalAlim2025) }}</span>
            </div>
          </div>
          <p class="hero__panel-foot">
            60 municipios · INEGI DENUE · Tianguis, fondas, cafeterías, restaurantes y bares
          </p>
        </aside>
      </div>

      <dl class="hero__stats">
        <div v-for="s in estadisticas" :key="s.etiqueta" class="hero__stat" :class="{ 'is-accent': s.destacado }">
          <dt class="hero__stat-value num">{{ s.valor }}</dt>
          <dd class="hero__stat-label">{{ s.etiqueta }}</dd>
          <p class="hero__stat-foot">{{ s.pie }}</p>
        </div>
      </dl>
    </div>
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  padding: 72px 0 64px;
  overflow: hidden;
}

@media (min-width: 768px) {
  .hero {
    padding: 104px 0 88px;
  }
}

.hero__glow {
  position: absolute;
  top: -220px;
  right: -140px;
  width: 560px;
  height: 560px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(245, 158, 11, 0.13), rgba(245, 158, 11, 0) 68%);
  pointer-events: none;
}

.hero__grid {
  display: grid;
  gap: 40px;
  position: relative;
}

@media (min-width: 1000px) {
  .hero__grid {
    grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr);
    gap: 56px;
    align-items: start;
  }
}

.hero__title {
  margin-top: 18px;
  font-size: clamp(32px, 5.6vw, 54px);
  line-height: 1.04;
  letter-spacing: -0.032em;
  font-weight: 600;
}

.hero__title-accent {
  display: block;
  color: var(--accent-700);
}

.hero__lead {
  margin-top: 22px;
  max-width: 56ch;
  font-size: 18px;
  font-weight: 300;
  line-height: 1.66;
  color: var(--ink-2);
}

.hero__lead strong {
  font-weight: 600;
  color: var(--ink);
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 30px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 11px 20px;
  border-radius: 999px;
  font-size: 14.5px;
  font-weight: 500;
  text-decoration: none;
  border: 1px solid transparent;
  transition: all 0.18s ease;
}

.btn--primary {
  background: var(--ink);
  color: #fff;
}

.btn--primary:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn--ghost {
  background: transparent;
  border-color: var(--line);
  color: var(--ink-2);
}

.btn--ghost:hover {
  border-color: var(--accent-line);
  color: var(--ink);
  transform: translateY(-1px);
}

/* panel lateral */
.hero__panel {
  padding: 24px;
  position: relative;
}

.hero__panel-label {
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: 0.11em;
  text-transform: uppercase;
  color: var(--muted);
}

.hero__panel-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin-top: 14px;
}

.hero__panel-value {
  font-size: 42px;
  line-height: 1;
  color: var(--accent-700);
}

.hero__panel-cap {
  margin-top: 5px;
  font-size: 13px;
  color: var(--muted);
}

.hero__panel-split {
  display: none;
  flex-direction: column;
  gap: 3px;
  font-family: var(--mono);
  font-size: 10.5px;
  color: var(--muted-2);
}

.hero__bars {
  margin-top: 22px;
  display: grid;
  gap: 11px;
}

.hero__bar {
  display: grid;
  grid-template-columns: 42px 1fr auto;
  gap: 11px;
  align-items: center;
}

.hero__bar-label {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--muted);
}

.hero__bar-track {
  height: 15px;
  border-radius: 7px;
  background: var(--line-soft);
  overflow: hidden;
}

.hero__bar-fill {
  height: 100%;
  border-radius: 7px;
  background: linear-gradient(90deg, var(--heat-2), var(--accent-600));
}

.hero__bar-fill--past {
  background: var(--past-soft);
}

.hero__bar-val {
  font-size: 13px;
  color: var(--ink-2);
}

.hero__panel-foot {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid var(--line-soft);
  font-size: 12px;
  line-height: 1.5;
  color: var(--muted);
}

/* tira de estadisticas */
.hero__stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1px;
  margin: 56px 0 0;
  background: var(--line);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
}

@media (min-width: 900px) {
  .hero__stats {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
}

.hero__stat {
  margin: 0;
  padding: 22px 20px;
  background: var(--surface);
}

.hero__stat-value {
  font-size: 27px;
  line-height: 1.1;
  color: var(--ink);
}

.hero__stat.is-accent .hero__stat-value {
  color: var(--accent-700);
}

.hero__stat-label {
  margin-top: 7px;
  font-size: 13px;
  font-weight: 500;
  line-height: 1.4;
  color: var(--ink-2);
}

.hero__stat-foot {
  margin-top: 6px;
  font-size: 11.5px;
  line-height: 1.45;
  color: var(--muted);
}
</style>
