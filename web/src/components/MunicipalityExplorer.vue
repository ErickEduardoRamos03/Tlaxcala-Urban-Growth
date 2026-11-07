<script setup>
import { ref, computed } from 'vue'
import { datos, fmtInt, fmt1, fmt2, fmtPct } from '../data/dataset.js'

const COLUMNAS = [
  { key: 'nombre', etiqueta: 'Municipio', tipo: 'texto' },
  { key: 'alim2010', etiqueta: 'Alim. 2010', tipo: 'num', formato: (v) => fmtInt(v) },
  { key: 'alim2025', etiqueta: 'Alim. 2025', tipo: 'num', formato: (v) => fmtInt(v) },
  { key: 'crec_alim_pct', etiqueta: 'Crec. %', tipo: 'num', formato: (v) => fmtPct(v) },
  { key: 'pob2020', etiqueta: 'Pob. 2020', tipo: 'num', formato: (v) => fmtInt(v) },
  { key: 'crec_pob_pct', etiqueta: 'Crec. pob. %', tipo: 'num', formato: (v) => fmtPct(v) },
  { key: 'foraneos_pct', etiqueta: 'Foraneos %', tipo: 'num', formato: (v) => fmt2(v) },
  { key: 'alim_por_hab_2025', etiqueta: 'Alim. x mil hab.', tipo: 'num', formato: (v) => fmt2(v) },
]

const busqueda = ref('')
const orden = ref({ key: 'crec_alim_pct', dir: 'desc' })
const soloTop = ref(false)

const filtrados = computed(() => {
  let filas = [...datos.municipios]
  if (soloTop.value) filas = filas.filter((m) => m.crec_alim_pct >= 100)
  const q = busqueda.value.trim().toLowerCase()
  if (q) {
    filas = filas.filter((m) => m.nombre.toLowerCase().includes(q))
  }
  const { key, dir } = orden.value
  filas.sort((a, b) => {
    const va = a[key]
    const vb = b[key]
    if (typeof va === 'string') return dir === 'asc' ? va.localeCompare(vb) : vb.localeCompare(va)
    return dir === 'asc' ? va - vb : vb - va
  })
  return filas
})

function ordenarPor(key) {
  if (orden.value.key === key) {
    orden.value = { key, dir: orden.value.dir === 'asc' ? 'desc' : 'asc' }
  } else {
    orden.value = { key, dir: 'desc' }
  }
}

function caret(key) {
  if (orden.value.key !== key) return ''
  return orden.value.dir === 'asc' ? '▲' : '▼'
}

const maxCrec = computed(() =>
  Math.max(...filtrados.value.map((m) => Math.abs(m.crec_alim_pct))),
)
</script>

<template>
  <div class="expl">
    <div class="expl__bar">
      <input
        v-model="busqueda"
        class="search"
        type="search"
        placeholder="Buscar municipio…"
        aria-label="Buscar municipio"
      />
      <div class="controls">
        <button
          type="button"
          class="chip"
          :aria-pressed="soloTop"
          @click="soloTop = !soloTop"
        >
          Solo +100% o mas
        </button>
      </div>
      <p class="expl__count">
        {{ filtrados.length }} de {{ datos.municipios.length }} municipios
      </p>
    </div>

    <div class="table-wrap expl__table">
      <table class="data">
        <thead>
          <tr>
            <th
              v-for="c in COLUMNAS"
              :key="c.key"
              class="sortable"
              :class="{ num: c.tipo === 'num' }"
              scope="col"
              @click="ordenarPor(c.key)"
            >
              {{ c.etiqueta }}<span class="sort-caret">{{ caret(c.key) }}</span>
            </th>
            <th scope="col" style="width: 180px">Intensidad</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="m in filtrados" :key="m.cve">
            <td
              v-for="c in COLUMNAS"
              :key="c.key"
              :class="{ num: c.tipo === 'num' }"
            >
              <template v-if="c.tipo === 'texto'">
                <span class="expl__name">{{ m.nombre }}</span>
              </template>
              <template v-else>
                <span :class="{ 'expl__hot': c.key === 'crec_alim_pct' && m.crec_alim_pct >= 100 }">
                  {{ c.formato(m[c.key]) }}
                </span>
              </template>
            </td>
            <td>
              <div class="expl__bar">
                <div class="expl__bar-track">
                  <div
                    class="expl__bar-fill"
                    :style="{ width: `${Math.min(100, (Math.abs(m.crec_alim_pct) / maxCrec) * 100)}%` }"
                  ></div>
                </div>
              </div>
            </td>
          </tr>
          <tr v-if="!filtrados.length">
            <td :colspan="COLUMNAS.length + 1" class="expl__empty">
              Ningun municipio coincide con la busqueda.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.expl__bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 14px;
  margin-bottom: 18px;
}

.expl__count {
  margin-left: auto;
  font-size: 13px;
  color: var(--muted);
}

.expl__table {
  max-height: 620px;
  overflow-y: auto;
}

.expl__name {
  font-weight: 500;
  color: var(--ink);
}

.expl__hot {
  color: var(--accent-700);
  font-weight: 500;
}

.expl__bar-track {
  height: 8px;
  border-radius: 5px;
  background: var(--line-soft);
  overflow: hidden;
}

.expl__bar-fill {
  height: 100%;
  border-radius: 5px;
  background: linear-gradient(90deg, var(--heat-2), var(--accent-600));
}

.expl__empty {
  padding: 34px 16px;
  text-align: center;
  color: var(--muted);
  font-size: 14px;
}
</style>
