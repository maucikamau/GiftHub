import ui from '@nuxt/ui/vue-plugin'
import { VueQueryPlugin } from '@tanstack/vue-query'
import { MotionPlugin } from '@vueuse/motion'
import { createPinia } from 'pinia'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './router/guards'
import '@/styles/main.css'
import 'overlayscrollbars/overlayscrollbars.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ui)
app.use(MotionPlugin)
app.use(VueQueryPlugin, { enableDevtoolsV6Plugin: true })

app.mount('#app')
