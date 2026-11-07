<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import SiteHeader from './components/SiteHeader.vue'
import HeroSection from './components/HeroSection.vue'
import KeyFindings from './components/KeyFindings.vue'
import ChoroplethMap from './components/ChoroplethMap.vue'
import DensityMap from './components/DensityMap.vue'
import GrowthRanking from './components/GrowthRanking.vue'
import FocusComparison from './components/FocusComparison.vue'
import MunicipalityExplorer from './components/MunicipalityExplorer.vue'
import Interpretation from './components/Interpretation.vue'
import Methodology from './components/Methodology.vue'
import SiteFooter from './components/SiteFooter.vue'

let observador = null

onMounted(() => {
  const objetivos = document.querySelectorAll('.reveal')
  observador = new IntersectionObserver(
    (entradas) => {
      entradas.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible')
          observador.unobserve(e.target)
        }
      })
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' },
  )
  objetivos.forEach((o) => observador.observe(o))
})

onBeforeUnmount(() => {
  if (observador) observador.disconnect()
})
</script>

<template>
  <SiteHeader />

  <main>
    <HeroSection />

    <!-- Hallazgos -->
    <section id="hallazgos" class="section section--tight">
      <div class="shell">
        <div class="section-head reveal">
          <p class="eyebrow">Lo que muestran los datos</p>
          <h2 class="section-title">Cuatro lecturas del mismo directorio</h2>
          <p class="section-lead">
            Antes de los mapas, cuatro conclusiones que resumen el analisis. Cada una
            tiene su propia visualizacion para que puedas contrastarla de un vistazo.
          </p>
        </div>
        <KeyFindings />
      </div>
    </section>

    <!-- Coropletico -->
    <section id="mapa" class="section">
      <div class="shell">
        <div class="section-head reveal">
          <p class="eyebrow">Los 60 municipios</p>
          <h2 class="section-title">La expansion vista desde arriba</h2>
          <p class="section-lead">
            Cambia la metrica para leer el mismo territorio desde cinco angulos: el
            crecimiento comercial, el volumen de establecimientos, su densidad por
            habitante, la poblacion foranea y el crecimiento demografico.
          </p>
        </div>
        <div class="reveal">
          <ChoroplethMap />
        </div>
      </div>
    </section>

    <!-- Expansion espacial -->
    <section id="expansion" class="section">
      <div class="shell">
        <div class="section-head reveal">
          <p class="eyebrow">Distribucion espacial</p>
          <h2 class="section-title">Donde se concentro la actividad</h2>
          <p class="section-lead">
            Cada circulo es una celda de unos 550 metros con al menos un establecimiento de
            alimentos y bebidas. Compara 2010 y 2025: el area cubierta se extendio hacia
            la periferia, no solo se intensifico en el centro.
          </p>
        </div>
        <div class="reveal">
          <DensityMap />
        </div>
      </div>
    </section>

    <!-- Ranking -->
    <section id="ranking" class="section">
      <div class="shell">
        <div class="section-head reveal">
          <p class="eyebrow">Ranking</p>
          <h2 class="section-title">Quien crecio mas</h2>
          <p class="section-lead">
            El orden cambia por completo segun la medida. En porcentaje lideran los
            municipios pequenos; en numero absoluto, los grandes. Las dos lecturas son
            necesarias y cuentan historias distintas.
          </p>
        </div>
        <div class="card card--pad reveal">
          <GrowthRanking />
        </div>
      </div>
    </section>

    <!-- Los cuatro municipios del cuaderno -->
    <section id="foco" class="section">
      <div class="shell">
        <div class="section-head reveal">
          <p class="eyebrow">El analisis original</p>
          <h2 class="section-title">Los cuatro municipios del cuaderno</h2>
          <p class="section-lead">
            Estas son las graficas del cuaderno de analisis, rehechas para el navegador.
            Las cifras son las mismas: el pipeline valida contra el cuaderno en cada
            construccion.
          </p>
        </div>
        <div class="reveal">
          <FocusComparison />
        </div>
      </div>
    </section>

    <!-- Explorador -->
    <section id="explorador" class="section">
      <div class="shell">
        <div class="section-head reveal">
          <p class="eyebrow">Explorador</p>
          <h2 class="section-title">Los 60 municipios, en detalle</h2>
          <p class="section-lead">
            Ordena por cualquier columna, filtra por nombre o por nivel de crecimiento.
            Todos los indicadores del portal, municipio por municipio.
          </p>
        </div>
        <div class="reveal">
          <MunicipalityExplorer />
        </div>
      </div>
    </section>

    <!-- Lectura -->
    <section id="lectura" class="section">
      <div class="shell">
        <div class="section-head reveal">
          <p class="eyebrow">Interpretacion</p>
          <h2 class="section-title">Que significan estos datos</h2>
          <p class="section-lead">
            Los numeros describen; la lectura los interroga. Esto es lo que el analisis
            sugiere y, sobre todo, lo que no puede afirmar.
          </p>
        </div>
        <div class="reveal">
          <Interpretation />
        </div>
      </div>
    </section>

    <!-- Metodologia -->
    <section id="metodologia" class="section">
      <div class="shell">
        <div class="section-head reveal">
          <p class="eyebrow">Metodologia</p>
          <h2 class="section-title">Como se construyó este portal</h2>
          <p class="section-lead">
            De los archivos .zip del INEGI a las graficas del navegador, con los criterios
            que se eligieron y los que se descartaron.
          </p>
        </div>
        <div class="reveal">
          <Methodology />
        </div>
      </div>
    </section>
  </main>

  <SiteFooter />
</template>
