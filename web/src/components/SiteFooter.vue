<script setup>
const anio = new Date().getFullYear()
</script>

<template>
  <footer class="footer">
    <div class="shell">
      <div class="footer__grid">
        <div>
          <p class="footer__brand">Crecimiento Urbano de Tlaxcala</p>
          <p class="footer__desc">
            Portal de visualizacion del analisis de gentrificacion comercial y dinamica
            demografica del estado de Tlaxcala, 2010-2025.
          </p>
        </div>

        <div>
          <p class="footer__label">Datos</p>
          <ul class="footer__list">
            <li>INEGI · ITER 2010 y 2020</li>
            <li>INEGI · DENUE 2010 y 2025</li>
            <li>INEGI · Marco Geoestadistico</li>
            <li>SHF · Indice de precios de vivienda</li>
          </ul>
        </div>

        <div>
          <p class="footer__label">Codigo</p>
          <ul class="footer__list">
            <li>
              <a href="https://github.com/ErickEduardoRamos03/Tlaxcala-Urban-Growth" target="_blank" rel="noopener">
                Repositorio en GitHub
              </a>
            </li>
            <li>
              <a href="https://github.com/ErickEduardoRamos03/Tlaxcala-Urban-Growth/blob/main/Analisis_Crecimiento_Urbano_Tlaxcala.ipynb" target="_blank" rel="noopener">
                Cuaderno de analisis
              </a>
            </li>
            <li>
              <a href="https://github.com/ErickEduardoRamos03/Tlaxcala-Urban-Growth/blob/main/tools/build_data.py" target="_blank" rel="noopener">
                Script de construccion de datos
              </a>
            </li>
          </ul>
        </div>
      </div>

      <p class="footer__legal">
        &copy; {{ anio }} Erick Eduardo Ramos · Datos de dominio publico del INEGI.
        Los resultados del analisis se presentan para fines academicos y de divulgacion.
      </p>
    </div>
  </footer>
</template>

<style scoped>
.footer__grid {
  display: grid;
  gap: 30px;
  grid-template-columns: repeat(12, minmax(0, 1fr));
}

.footer__grid > *:first-child {
  grid-column: span 12;
}

.footer__grid > *:nth-child(2) {
  grid-column: span 12;
}

.footer__grid > *:last-child {
  grid-column: span 12;
}

@media (min-width: 860px) {
  .footer__grid > *:first-child {
    grid-column: span 6;
  }
  .footer__grid > *:nth-child(2) {
    grid-column: span 3;
  }
  .footer__grid > *:last-child {
    grid-column: span 3;
  }
}

.footer__brand {
  font-size: 15px;
  font-weight: 600;
  color: var(--ink);
}

.footer__desc {
  margin-top: 8px;
  max-width: 46ch;
  font-size: 13.5px;
  line-height: 1.6;
  color: var(--muted);
}

.footer__label {
  font-family: var(--mono);
  font-size: 10.5px;
  letter-spacing: 0.11em;
  text-transform: uppercase;
  color: var(--muted-2);
}

.footer__list {
  margin: 12px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 7px;
  font-size: 13.5px;
  color: var(--ink-2);
}

.footer__legal {
  margin-top: 34px;
  padding-top: 20px;
  border-top: 1px solid var(--line);
  font-size: 12.5px;
  color: var(--muted-2);
}
</style>
