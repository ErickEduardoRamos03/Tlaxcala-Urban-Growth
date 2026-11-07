<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const enlaces = [
  { id: 'hallazgos', label: 'Hallazgos' },
  { id: 'mapa', label: 'Mapa' },
  { id: 'expansion', label: 'Expansion' },
  { id: 'ranking', label: 'Ranking' },
  { id: 'explorador', label: 'Explorador' },
  { id: 'lectura', label: 'Lectura' },
  { id: 'metodologia', label: 'Metodologia' },
]

const abierto = ref(false)
const activo = ref('')
const desplazado = ref(false)

function alDesplazar() {
  desplazado.value = window.scrollY > 24
  const corte = window.scrollY + 140
  activo.value = ''
  for (const e of enlaces) {
    const el = document.getElementById(e.id)
    if (el && el.offsetTop <= corte) activo.value = e.id
  }
}

onMounted(() => {
  alDesplazar()
  window.addEventListener('scroll', alDesplazar, { passive: true })
})
onBeforeUnmount(() => window.removeEventListener('scroll', alDesplazar))
</script>

<template>
  <header class="hd" :class="{ 'hd--scrolled': desplazado }">
    <div class="shell hd__inner">
      <a href="#inicio" class="hd__brand">
        <span class="hd__mark" aria-hidden="true">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 21h18" />
            <path d="M5 21V10" />
            <path d="M10 21V4" />
            <path d="M15 21v-8" />
            <path d="M20 21v-5" />
          </svg>
        </span>
        <span class="hd__title">
          Crecimiento Urbano
          <span class="hd__place">de Tlaxcala</span>
        </span>
      </a>

      <nav class="hd__nav" aria-label="Secciones">
        <a
          v-for="e in enlaces"
          :key="e.id"
          :href="`#${e.id}`"
          class="hd__link"
          :class="{ 'is-active': activo === e.id }"
        >
          {{ e.label }}
        </a>
      </nav>

      <button
        class="hd__toggle"
        type="button"
        :aria-expanded="abierto"
        aria-label="Alternar navegacion"
        @click="abierto = !abierto"
      >
        <svg v-if="!abierto" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <path d="M3 6h18M3 12h18M3 18h18" />
        </svg>
        <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <path d="M18 6 6 18M6 6l12 12" />
        </svg>
      </button>
    </div>

    <div v-if="abierto" class="hd__sheet">
      <a
        v-for="e in enlaces"
        :key="e.id"
        :href="`#${e.id}`"
        class="hd__sheet-link"
        @click="abierto = false"
      >
        {{ e.label }}
      </a>
    </div>
  </header>
</template>

<style scoped>
.hd {
  position: sticky;
  top: 0;
  z-index: 900;
  background: rgba(250, 250, 250, 0.86);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s ease, background 0.2s ease;
}

.hd--scrolled {
  border-bottom-color: var(--line);
  background: rgba(250, 250, 250, 0.95);
}

.hd__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  height: 64px;
}

.hd__brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--ink);
}

.hd__mark {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 9px;
  background: var(--accent-soft);
  border: 1px solid var(--accent-line);
  color: var(--accent-700);
}

.hd__title {
  font-size: 14.5px;
  font-weight: 600;
  letter-spacing: -0.015em;
  line-height: 1.15;
}

.hd__place {
  display: block;
  font-size: 11px;
  font-weight: 400;
  color: var(--muted);
  letter-spacing: 0.01em;
}

.hd__nav {
  display: none;
  align-items: center;
  gap: 2px;
}

.hd__link {
  padding: 7px 11px;
  border-radius: 8px;
  font-size: 13.5px;
  font-weight: 500;
  color: var(--muted);
  text-decoration: none;
  transition: color 0.16s ease, background 0.16s ease;
}

.hd__link:hover {
  color: var(--ink);
  background: var(--surface-2);
}

.hd__link.is-active {
  color: var(--ink);
  background: var(--accent-soft);
}

.hd__toggle {
  display: grid;
  place-items: center;
  width: 38px;
  height: 38px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: var(--surface);
  color: var(--ink);
  transition: border-color 0.16s ease;
}

.hd__toggle:hover {
  border-color: var(--accent-line);
}

.hd__sheet {
  display: grid;
  padding: 8px 24px 18px;
  border-top: 1px solid var(--line);
  background: var(--bg);
}

.hd__sheet-link {
  padding: 11px 4px;
  border-bottom: 1px solid var(--line-soft);
  font-size: 15px;
  font-weight: 500;
  color: var(--ink-2);
  text-decoration: none;
}

.hd__sheet-link:last-child {
  border-bottom: none;
}

@media (min-width: 1000px) {
  .hd__nav {
    display: flex;
  }

  .hd__toggle,
  .hd__sheet {
    display: none;
  }
}
</style>
