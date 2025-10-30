import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue';
import RegistrationView from '@/views/RegistrationView.vue';
import RegistrationDonorView from '@/views/RegistrationDonorView.vue';
import RegistrationRecipientView from '@/views/RegistrationRecipientView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/registracija',
      name: 'registracija',
      component: RegistrationView,
    },
    {
      path: '/registracija/donator',
      name: 'registracija-donator',
      component: RegistrationDonorView,
    },
    {
      path: '/registracija/primatelj',
      name: 'registracija-primatelj',
      component: RegistrationRecipientView,
    },
  ],
})

export default router
