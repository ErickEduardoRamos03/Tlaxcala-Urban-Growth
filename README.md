# Tlaxcala-Urban-Growth 🌆
### Análisis de Gentrificación y Evolución Económica (2010 - 2025)

Este repositorio contiene un análisis exhaustivo basado en **Ciencia de Datos** sobre la transformación urbana de la capital de Tlaxcala. El proyecto utiliza microdatos oficiales para identificar patrones de gentrificación comercial y el impacto en el costo de la vivienda.

## 🚀 Objetivo del Proyecto
Determinar la correlación entre el crecimiento de unidades económicas de servicios y el aumento desproporcionado en los precios de los bienes raíces, contrastándolo con el crecimiento poblacional real de la región.

## 🛠️ Stack Tecnológico

**Analisis (Python)**
* **Lenguaje:** Python 3.10+ (ejecución local con Jupyter / VS Code)
* **Librerías principales:**
    * `Pandas` para manipulación de grandes volúmenes de datos.
    * `Seaborn` & `Matplotlib` para visualización estadística.
    * `Zipfile` & `Pathlib` para automatización de la gestión de archivos.
* **Fuentes de Datos:** INEGI (ITER y DENUE) y Sociedad Hipotecaria Federal (SHF).

**Portal (JavaScript)**
* **Lenguaje:** Vue 3 (Composition API) + Vite
* **Visualización:** Chart.js para las gráficas, Leaflet para los mapas (coroplético y densidad)
* **Datos:** JSON precalculado por `tools/build_data.py`, sin backend


## 📊 Hallazgos Principales
* **Vivienda más cara que el promedio nacional:** el índice SHF de precios de vivienda cerró 2025 con un **+12.0%** en Tlaxcala frente al **+8.7%** promedio nacional, es decir **+3.3 puntos porcentuales** por encima.
* **Gentrificación Comercial:** el DENUE muestra un desplazamiento de comercios tradicionales por giros enfocados al turismo y sectores de mayor poder adquisitivo. Crecimiento de establecimientos de alimentos y bebidas entre 2010 y 2025: **Huamantla +56.9%**, **Tlaxcala +48.0%**, Chiautempan +41.3% y Apizaco +23.6%.
* **Recambio demográfico:** en 2020 el **4.57%** de la población de Tlaxcala provenía de otra entidad, el valor más alto de los cuatro municipios analizados, frente a un crecimiento poblacional 2010-2020 de **+11.25%** (Apizaco +5.53%, Chiautempan +10.68%, Huamantla +16.22%).
* **ETL reproducible:** el notebook descomprime y limpia los datos de forma automática, de modo que el análisis completo puede regenerarse desde cero en cualquier máquina con `Run All`.

> **Nota sobre la cifra del 48.0%:** corresponde al **crecimiento de establecimientos de alimentos y bebidas en el municipio de Tlaxcala**, *no* al índice de precios de vivienda (que es el +12.0% de la SHF). Las versiones anteriores de este README confundían ambos indicadores.

## 📂 Estructura del Repositorio
* `Analisis_Crecimiento_Urbano_Tlaxcala.ipynb`: notebook principal con el ciclo completo de vida del dato (Ingesta, Limpieza, EDA, Conclusiones).
* `/data`: datasets crudos del INEGI (ITER 2010/2020 y DENUE 2010-2025) en formato `.zip`.
* `/tools/build_data.py`: pipeline que convierte los `.zip` crudos en el JSON que consume el portal.
* `/web`: portal interactivo en Vue 3 (fuente del sitio publicado en GitHub Pages).
* `/extracted`: archivos descomprimidos — se genera al ejecutar, no se versiona.
* `/output`: gráficas exportadas en PNG — se genera al ejecutar, no se versiona.
* `validar.py`: comprueba que el notebook se ejecuta sin errores y que las cifras publicadas se reproducen.

## 🌐 Portal interactivo

**👉 [erickeduaramos03.github.io/Tlaxcala-Urban-Growth](https://erickeduaramos03.github.io/Tlaxcala-Urban-Growth/)**

El cuaderno responde preguntas puntuales; el portal deja recorrer el territorio completo. Incluye:

* **Mapa coroplético** de los 60 municipios, con cinco métricas intercambiables: crecimiento comercial, volumen de establecimientos, densidad por habitante, población foránea y crecimiento demográfico.
* **Mapa de densidad** con conmutador 2010 / 2025 que muestra la expansión espacial de los establecimientos.
* **Ranking** por crecimiento porcentual y por aumento absoluto, dos lecturas que cuentan historias distintas.
* **Comparación de los cuatro municipios** del cuaderno original, con las mismas cifras.
* **Explorador** de los 60 municipios con ordenación por cualquier columna, búsqueda y filtro por umbral de crecimiento.
* **Interpretación** de los resultados, con sus límites explícitos.

### Regenerar los datos del portal

```bash
python tools/build_data.py
```

El script procesa los `.zip` de `data/`, descarga la geometría municipal del INEGI (con caché en `tools/.cache/`) y escribe `web/src/data/datos.json`. **Falla con código de error si las cifras de los cuatro municipios centrales dejan de coincidir con las publicadas en el cuaderno**, de modo que el portal nunca puede contradecir al análisis.

### Desarrollo local del portal

```bash
cd web
npm install
npm run dev      # servidor de desarrollo en http://localhost:5173
npm run build    # genera web/dist
```


## 🚀 Ejecución Local

```bash
# 1. Crear el entorno virtual
python -m venv .venv

# 2. Activarlo
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Lanzar Jupyter
jupyter lab
```

Abre `Analisis_Crecimiento_Urbano_Tlaxcala.ipynb` y ejecuta todas las celdas (`Run All`). El notebook detecta solo la raíz del proyecto, descomprime los `.zip` de `data/` dentro de `extracted/` y exporta las cuatro gráficas en `output/`.

En VS Code basta con abrir la carpeta del repositorio y seleccionar el intérprete `.venv` como kernel.

### Verificar la reproducibilidad

```bash
python validar.py
```

El script confirma que no hay errores de ejecución, que se generan las 4 gráficas y que los valores de la tabla DENUE coinciden con los publicados.

---
## 👤 Autor
**Erick Eduardo Ramos** *Científico de Datos | Entusiasta de la Historia y Cultura Tlaxcalteca*

¿Buscas un análisis de datos con impacto real? ¡Contáctame para colaborar en proyectos freelance de análisis de mercado o ciencia de datos aplicada!
