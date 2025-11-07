import ui from '@nuxt/ui/vue-plugin'
import { MotionPlugin } from '@vueuse/motion'
import { createPinia } from 'pinia'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import '@/styles/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ui)
app.use(MotionPlugin)

app.mount('#app')
