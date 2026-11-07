import raw from './datos.json'

export const datos = raw

export const municipios = raw.municipios

export const porCve = Object.fromEntries(raw.municipios.map((m) => [m.cve, m]))

export const porNombre = Object.fromEntries(
  raw.municipios.map((m) => [normaliza(m.nombre), m]),
)

/** Busca un municipio por nombre, ignorando acentos, mayusculas y espacios. */
export function buscar(nombre) {
  return porNombre[normaliza(nombre)] || null
}

export function normaliza(s) {
  return String(s ?? '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
    .toUpperCase()
}

const nf = new Intl.NumberFormat('es-MX')
const nf1 = new Intl.NumberFormat('es-MX', { maximumFractionDigits: 1 })
const nf2 = new Intl.NumberFormat('es-MX', { minimumFractionDigits: 2, maximumFractionDigits: 2 })

export const fmtInt = (n) => nf.format(Math.round(Number(n) || 0))
export const fmt1 = (n) => nf1.format(Number(n) || 0)
export const fmt2 = (n) => nf2.format(Number(n) || 0)

/** Formatea un porcentaje con signo explicito. */
export function fmtPct(n, decimales = 1) {
  const v = Number(n) || 0
  const s = decimales === 2 ? fmt2(v) : fmt1(v)
  return `${v > 0 ? '+' : ''}${s}%`
}

/** Totales estatales de alimentos y bebidas. */
export const totalAlim2010 = raw.municipios.reduce((a, m) => a + m.alim2010, 0)
export const totalAlim2025 = raw.municipios.reduce((a, m) => a + m.alim2025, 0)
export const crecTotalPct = ((totalAlim2025 / totalAlim2010 - 1) * 100)

/** Los cuatro municipios del analisis original del notebook. */
export const FOCUS = ['Tlaxcala', 'Apizaco', 'Chiautempan', 'Huamantla'].map(buscar).filter(Boolean)

/** Municipios con mayor crecimiento porcentual. */
export const topCrecimiento = [...raw.municipios].sort((a, b) => b.crec_alim_pct - a.crec_alim_pct)

/** Municipios con mayor aumento absoluto de establecimientos. */
export const topAbsoluto = [...raw.municipios]
  .map((m) => ({ ...m, delta: m.alim2025 - m.alim2010 }))
  .sort((a, b) => b.delta - a.delta)

/** Umbrales por defecto de la rampa secuencial del coropletico. */
export const UMBRALES = [0, 30, 50, 70, 95, 130, Infinity]

/** Rampa secuencial del coropletico, de bajo a alto. */
export const RAMP = [
  '#f4f4f5',
  '#fef3c7',
  '#fcd34d',
  '#f59e0b',
  '#d97706',
  '#b45309',
]

/**
 * Devuelve el color de la rampa para un valor, dados los cortes del tramo.
 * `cortes` tiene un elemento mas que `RAMP`: [min, ..., max].
 */
export function colorPorCortes(valor, cortes) {
  for (let i = 0; i < cortes.length - 1; i++) {
    if (valor < cortes[i + 1]) return RAMP[i]
  }
  return RAMP[RAMP.length - 1]
}

/** Color divergente para variaciones (positivo / negativo). */
export function colorDivergente(valor, max = 200) {
  if (valor >= 0) {
    const t = Math.min(1, valor / max)
    return `rgba(245, 158, 11, ${0.16 + t * 0.74})`
  }
  const t = Math.min(1, Math.abs(valor) / max)
  return `rgba(100, 116, 139, ${0.16 + t * 0.5})`
}
