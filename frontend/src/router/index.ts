import { createRouter, createWebHistory } from 'vue-router'
import DonationsView from '@/views/DonationsView.vue'
import EditListingView from '@/views/EditListingView.vue'
import HomeView from '@/views/home/HomeView.vue'
import ListingView from '@/views/ListingView.vue'
import LoginView from '@/views/LoginView.vue'
import LogoutView from '@/views/LogoutView.vue'
import MyListingsView from '@/views/MyListingsView.vue'
import NewListingView from '@/views/NewListingView.vue'
import NotFound from '@/views/NotFound.vue'
import OnboardingView from '@/views/OnboardingView.vue'
import ProfileView from '@/views/ProfileView.vue'

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
      meta: { unauthenticatedOnly: true },
    },
    {
      path: '/odjava',
      name: 'odjava',
      component: LogoutView,
    },
    {
      path: '/onboarding',
      name: 'onboarding',
      component: OnboardingView,
    },
    {
      path: '/profil',
      name: 'profil',
      component: ProfileView,
    },
    {
      path: '/oglasi/novi',
      name: 'oglasi-novi',
      component: NewListingView,
    },
    {
      path: '/oglasi/ja',
      name: 'moji-oglasi',
      component: MyListingsView,
    },
    {
      path: '/oglasi/:id',
      name: 'pregled-oglasa',
      component: ListingView,
    },
    {
      path: '/oglasi/:id/uredi',
      name: 'uredi-oglas',
      component: EditListingView,
    },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
  ],
})

export default router
