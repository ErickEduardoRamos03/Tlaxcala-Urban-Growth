<script setup>
import { computed } from 'vue'
import { topCrecimiento, topAbsoluto, FOCUS, fmtInt, fmt1, fmtPct } from '../data/dataset.js'

const sp = computed(() => topAbsoluto.find((m) => m.nombre === 'San Pablo del Monte'))
const xalt = computed(() => topCrecimiento.find((m) => m.nombre === 'Xaltocan'))

/** Poblacion 2020 de los cuatro municipios del analisis original. */
const pobFoco = computed(() => FOCUS.reduce((a, m) => a + m.pob2020, 0))

/** Crecimiento comercial promedio de esos cuatro municipios. */
const crecFoco = computed(
  () => FOCUS.reduce((a, m) => a + m.crec_alim_pct, 0) / FOCUS.length,
)

const tlaxcala = computed(() => FOCUS.find((m) => m.nombre === 'Tlaxcala'))
</script>

<template>
  <div class="read">
    <div class="read__grid">
      <article class="read__item">
        <span class="read__num">01</span>
        <h3 class="read__title">El centro cambio de funcion, no de tamano</h3>
        <p class="read__text">
          Los cuatro municipios analizados en el cuaderno original siguen siendo el motor
          demografico del estado: concentran {{ fmtInt(pobFoco) }} habitantes, y sus
          unidades de alimentos y bebidas crecieron en torno al
          {{ fmtPct(crecFoco) }} en quince anos. Pero el detalle importante es que en
          Tlaxcala el {{ fmt1(tlaxcala?.foraneos_pct) }}% de su poblacion de 2020 venia de
          otra entidad. No es solo gente nueva: es gente que sustituyo a quien vivia ahi
          antes.
        </p>
      </article>

      <article class="read__item">
        <span class="read__num">02</span>
        <h3 class="read__title">La frontera de la gentrificacion se movio</h3>
        <p class="read__text">
          El dato que el cuaderno original no alcanzaba a ver es que el mayor crecimiento
          porcentual ya no esta en la capital.
          {{ xalt?.nombre }} multiplico por {{ fmt1(xalt?.alim2025 / xalt?.alim2010) }} sus
          establecimientos de alimentos y bebidas, y detras de el aparecen Tepeyanco,
          Santa Cruz Tlaxcala y Tlaxco: el cordon periurbano que corona a la capital.
        </p>
      </article>

      <article class="read__item">
        <span class="read__num">03</span>
        <h3 class="read__title">San Pablo del Monte es el caso mas completo</h3>
        <p class="read__text">
          Paso de {{ fmtInt(sp?.alim2010) }} a {{ fmtInt(sp?.alim2025) }} establecimientos
          ({{ fmtPct(sp?.crec_alim_pct) }}) y es, al mismo tiempo, el municipio con mayor
          crecimiento porcentual y con mayor aumento absoluto. Cuando coinciden las dos
          medidas, la senal es dificil de explicar por dinamicas de escala.
        </p>
      </article>

      <article class="read__item">
        <span class="read__num">04</span>
        <h3 class="read__title">El suelo se encarece mas rapido que la gente</h3>
        <p class="read__text">
          El indice SHF cierra 2025 con +12.0% en Tlaxcala frente al +8.7% nacional. En
          paralelo, la poblacion de la capital crecio {{ fmtPct(tlaxcala?.crec_pob_pct) }}
          en una decada. La brecha entre lo que sube el precio del suelo y lo que crece la
          poblacion es precisamente la firma economica de la gentrificacion.
        </p>
      </article>
    </div>

    <aside class="read__caveat">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <circle cx="12" cy="12" r="10" />
        <path d="M12 16v-4" />
        <path d="M12 8h.01" />
      </svg>
      <p>
        <strong>Una advertencia sobre la lectura.</strong> El DENUE registra
        <em>establecimientos</em>, no empleo formal ni facturacion. Un crecimiento de
        unidades de alimentos y bebidas es compatible con mas turnos, con mas
        informalidad y con mas precariedad, no solo con mas consumo de clase media.
        Los datos muestran donde se concentro la actividad; no demuestran quien la
        sostiene ni a costa de quien.
      </p>
    </aside>
  </div>
</template>

<style scoped>
.read__grid {
  display: grid;
  gap: 28px;
  grid-template-columns: repeat(12, minmax(0, 1fr));
}

.read__item {
  grid-column: span 12;
}

@media (min-width: 900px) {
  .read__item {
    grid-column: span 6;
  }
}

.read__num {
  display: inline-block;
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.1em;
  color: var(--accent-600);
  padding-bottom: 10px;
  border-bottom: 2px solid var(--accent-line);
}

.read__title {
  margin-top: 16px;
  font-size: 19px;
  line-height: 1.25;
}

.read__text {
  margin-top: 12px;
  font-size: 15px;
  font-weight: 300;
  line-height: 1.68;
  color: var(--ink-2);
}

.read__caveat {
  display: flex;
  gap: 14px;
  margin-top: 44px;
  padding: 22px 24px;
  border: 1px solid var(--line);
  border-left: 3px solid var(--accent);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--ink-2);
}

.read__caveat svg {
  flex-shrink: 0;
  color: var(--accent-600);
  margin-top: 2px;
}

.read__caveat p {
  font-size: 14px;
  line-height: 1.65;
  font-weight: 300;
}

.read__caveat strong {
  font-weight: 600;
  color: var(--ink);
}

.read__caveat em {
  font-style: italic;
}
</style>
