import { createRouter, createWebHistory } from 'vue-router'
import DonationsView from '@/views/DonationsView.vue'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import NewListingConfirmView from '@/views/NewListingConfirmView.vue'
import NewListingView from '@/views/NewListingView.vue'
import NotFound from '@/views/NotFound.vue'
import OnboardingView from '@/views/OnboardingView.vue'

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
      path: '/onboarding',
      name: 'onboarding',
      component: OnboardingView,
    },
    {
      path: '/oglasi/novi',
      name: 'oglasi-novi',
      component: NewListingView,
    },
    {
      path: '/oglasi/novi/potvrda',
      name: 'oglasi-novi-potvrda',
      component: NewListingConfirmView,
    },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
  ],
})

export default router
