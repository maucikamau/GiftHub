import { fileURLToPath, URL } from 'node:url'
import ui from '@nuxt/ui/vite'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  build: {
    assetsDir: 'static',
  },
  plugins: [
    vue(),
    ui({
      colorMode: false,
      theme: {
        colors: [
          'primary',
          'secondary',
          'info',
          'success',
          'warning',
          'error',
          'surface',
        ],
      },
      ui: {
        colors: {
          primary: 'amber',
          neutral: 'beige',
        },
      },
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
