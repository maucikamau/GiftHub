import type { App } from 'vue'
import { QueryClient, VueQueryPlugin } from '@tanstack/vue-query'

export const qc = new QueryClient()

export function installVueQuery(app: App) {
  app.use(VueQueryPlugin, {
    queryClient: qc,
    enableDevtoolsV6Plugin: true,
  })
}
