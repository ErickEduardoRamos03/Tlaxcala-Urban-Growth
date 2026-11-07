<script setup>
import { computed } from 'vue'
import {
  topCrecimiento,
  topAbsoluto,
  FOCUS,
  fmtInt,
  fmt1,
  fmt2,
  fmtPct,
  totalAlim2010,
  totalAlim2025,
} from '../data/dataset.js'

const maxCrec = computed(() => topCrecimiento[0].crec_alim_pct)
const maxAbs = computed(() => topAbsoluto[0].delta)
</script>

<template>
  <div class="find">
    <!-- 1. La periferia crece mas rapido en porcentaje -->
    <article class="card card--pad find__a">
      <p class="eyebrow">Hallazgo 01</p>
      <h3 class="card-title find__title">El centro no lleva el ritmo</h3>
      <p class="card-sub">
        En porcentaje, los municipios que mas crecieron son los pequenos de la periferia.
        Tlaxcala, con el mayor volumen, queda en la zona media del ranking.
      </p>
      <div class="find__bench">
        <div v-for="m in topCrecimiento.slice(0, 5)" :key="m.cve" class="bench">
          <span class="bench-label">{{ m.nombre }}</span>
          <div class="bench-track">
            <div class="bench-fill" :style="{ width: `${(m.crec_alim_pct / maxCrec) * 100}%` }"></div>
          </div>
          <span class="bench-val">{{ fmtPct(m.crec_alim_pct) }}</span>
        </div>
        <div class="bench bench--sep">
          <span class="bench-label">Tlaxcala <em>(capital)</em></span>
          <div class="bench-track">
            <div class="bench-fill" :style="{ width: `${(48.016701 / maxCrec) * 100}%` }"></div>
          </div>
          <span class="bench-val">{{ fmtPct(48.016701) }}</span>
        </div>
      </div>
    </article>

    <!-- 2. El volumen absoluto si lo lleva la capital -->
    <article class="card card--pad find__b">
      <p class="eyebrow">Hallazgo 02</p>
      <h3 class="card-title find__title">En volumen, la capital si manda</h3>
      <p class="card-sub">
        Huamantla, San Pablo del Monte y Tlaxcala concentran el mayor numero de
        establecimientos ganados. El crecimiento porcentual y el absoluto cuentan
        historias distintas, y por eso el portal muestra ambos.
      </p>
      <div class="find__bench">
        <div v-for="m in topAbsoluto.slice(0, 4)" :key="m.cve" class="bench">
          <span class="bench-label">{{ m.nombre }}</span>
          <div class="bench-track">
            <div class="bench-fill" :style="{ width: `${(m.delta / maxAbs) * 100}%` }"></div>
          </div>
          <span class="bench-val">+{{ fmtInt(m.delta) }}</span>
        </div>
      </div>
      <p class="find__note">
        Dato clave: <strong>San Pablo del Monte</strong> paso de
        {{ fmtInt(topAbsoluto.find((m) => m.nombre === 'San Pablo del Monte')?.alim2010) }} a
        {{ fmtInt(topAbsoluto.find((m) => m.nombre === 'San Pablo del Monte')?.alim2025) }}
        establecimientos, con un crecimiento de
        <strong>{{ fmtPct(topAbsoluto.find((m) => m.nombre === 'San Pablo del Monte')?.crec_alim_pct) }}</strong>.
      </p>
    </article>

    <!-- 3. La vivienda corre mas rapido que la demografia -->
    <article class="card card--pad find__c">
      <p class="eyebrow">Hallazgo 03</p>
      <h3 class="card-title find__title">La vivienda se encarece por encima del pais</h3>
      <p class="card-sub">
        El indice de precios de la vivienda de la SHF subio mas en Tlaxcala que en el
        promedio nacional, mientras la poblacion crecia a un ritmo modesto.
      </p>
      <div class="find__shf">
        <div class="find__shf-row">
          <span class="find__shf-label">Tlaxcala</span>
          <div class="find__shf-track">
            <div class="find__shf-fill" style="width: 100%; background: #f59e0b"></div>
          </div>
          <span class="find__shf-val num">+12.0%</span>
        </div>
        <div class="find__shf-row">
          <span class="find__shf-label">Nacional</span>
          <div class="find__shf-track">
            <div class="find__shf-fill" style="width: 72.5%; background: #9aa3b2"></div>
          </div>
          <span class="find__shf-val num">+8.7%</span>
        </div>
      </div>
      <p class="find__note">
        Fuente: Sociedad Hipotecaria Federal, indice de precios de la vivienda en Mexico,
        cierre del cuarto trimestre de 2025.
      </p>
    </article>

    <!-- 4. Recambio demografico en los cuatro municipios del analisis -->
    <article class="card card--pad find__d">
      <p class="eyebrow">Hallazgo 04</p>
      <h3 class="card-title find__title">Cambio de composicion, no solo crecimiento</h3>
      <p class="card-sub">
        En el municipio de Tlaxcala el 4.57% de la poblacion de 2020 venia de otra entidad:
        el valor mas alto de los cuatro municipios analizados. No es solo que crezca,
        es que se reemplaza.
      </p>
      <div class="find__bench">
        <div v-for="m in FOCUS" :key="m.cve" class="bench">
          <span class="bench-label">{{ m.nombre }}</span>
          <div class="bench-track">
            <div
              class="bench-fill"
              :style="{ width: `${(m.foraneos_pct / 5) * 100}%`, background: 'linear-gradient(90deg,#fbbf24,#b45309)' }"
            ></div>
          </div>
          <span class="bench-val">{{ fmt2(m.foraneos_pct) }}%</span>
        </div>
      </div>
      <p class="find__note">
        Poblacion foranea calculada con PRESOE15 del ITER 2020 sobre POBTOT municipal.
      </p>
    </article>
  </div>
</template>

<style scoped>
.find {
  display: grid;
  gap: 18px;
  grid-template-columns: repeat(12, minmax(0, 1fr));
}

.find__a {
  grid-column: span 12;
}

.find__b {
  grid-column: span 12;
}

.find__c {
  grid-column: span 12;
}

.find__d {
  grid-column: span 12;
}

@media (min-width: 900px) {
  .find__a {
    grid-column: span 7;
  }
  .find__b {
    grid-column: span 5;
  }
  .find__c {
    grid-column: span 5;
  }
  .find__d {
    grid-column: span 7;
  }
}

.find__title {
  margin-top: 10px;
  font-size: 18px;
}

.find__bench {
  margin-top: 22px;
}

.bench--sep {
  margin-top: 10px;
  padding-top: 12px;
  border-top: 1px dashed var(--line);
}

.bench-label em {
  font-style: normal;
  font-size: 11px;
  color: var(--muted-2);
}

.find__note {
  margin-top: 20px;
  padding-top: 14px;
  border-top: 1px solid var(--line-soft);
  font-size: 12.5px;
  line-height: 1.55;
  color: var(--muted);
}

.find__note strong {
  color: var(--ink-2);
  font-weight: 600;
}

.find__shf {
  margin-top: 22px;
  display: grid;
  gap: 12px;
}

.find__shf-row {
  display: grid;
  grid-template-columns: 84px 1fr 64px;
  gap: 12px;
  align-items: center;
}

.find__shf-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--ink-2);
}

.find__shf-track {
  height: 15px;
  border-radius: 7px;
  background: var(--line-soft);
  overflow: hidden;
}

.find__shf-fill {
  height: 100%;
  border-radius: 7px;
}

.find__shf-val {
  font-size: 13px;
  text-align: right;
  color: var(--ink);
}
</style>
