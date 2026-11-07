import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// GitHub Pages sirve el portal bajo /Tlaxcala-Urban-Growth/.
// Para desarrollo local, vite ignora el base y sirve en la raiz.
export default defineConfig({
  base: '/Tlaxcala-Urban-Growth/',
  plugins: [vue()],
  server: {
    port: 5173,
    host: '127.0.0.1',
    open: false,
  },
  preview: {
    port: 4173,
    host: '127.0.0.1',
    open: false,
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    chunkSizeWarningLimit: 1200,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue'],
          charts: ['chart.js'],
          maps: ['leaflet'],
        },
      },
    },
  },
})
