import { createRouter, createWebHistory } from 'vue-router'
import DonationsView from '@/views/DonationsView.vue'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import NotFound from '@/views/NotFound.vue'
import RegistrationAssociationView from '@/views/RegistrationAssociationView.vue'
import RegistrationDonorView from '@/views/RegistrationDonorView.vue'
import RegistrationPrivateUserView from '@/views/RegistrationPrivateUserView.vue'
import RegistrationRecipientView from '@/views/RegistrationRecipientView.vue'
import RegistrationView from '@/views/RegistrationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/donacije',
      name: 'donacije',
      component: DonationsView,
    },
    {
      path: '/prijava',
      name: 'prijava',
      component: LoginView,
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
    {
      path: '/registracija/privatniKorisnik',
      name: 'registracija-privatniKorisnik',
      component: RegistrationPrivateUserView,
    },
    {
      path: '/registracija/udruga',
      name: 'registracija-udruga',
      component: RegistrationAssociationView,
    },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
  ],
})

export default router
