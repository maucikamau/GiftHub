import type { Plugin } from 'vite'
import process from 'node:process'
import { fileURLToPath, URL } from 'node:url'
import ui from '@nuxt/ui/vite'
import vue from '@vitejs/plugin-vue'
import { defineConfig, loadEnv } from 'vite'

// Custom plugin to replace Jinja2 template variables with environment variables in dev mode
function replaceTemplateVariables(): Plugin {
  return {
    name: 'replace-template-variables',
    transformIndexHtml(html) {
      if (process.env.NODE_ENV !== 'development')
        return html
      process.env = { ...process.env, ...loadEnv('development', process.cwd()) }

      // Replace {{ stream_api_key }} with the actual environment variable value
      return html.replace(
        /\{\{\s*stream_api_key\s*\}\}/g,
        process.env.VITE_STREAM_CHAT_API_KEY || '',
      )
    },
  }
}

// https://vite.dev/config/
export default defineConfig({
  build: {
    assetsDir: 'static',
  },
  plugins: [
    replaceTemplateVariables(),
    vue(),
    ui({
      colorMode: false,
      theme: {
        colors: [
          'primary',
          'secondary',
          'success',
          'warning',
          'error',
          'surface',
        ],
      },
      ui: {
        button: {
          slots: {
            base: 'cursor-pointer',
          },
        },
        colors: {
          primary: 'amber',
          neutral: 'stone',
          surface: 'surface',
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
