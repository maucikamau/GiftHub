import { createRouter, createWebHistory } from 'vue-router'
import RegisteredUserLayout from '@/layouts/RegisteredUserLayout.vue'
import ActiveDonationsView from '@/views/ActiveDonationsView.vue'
import CampaignsView from '@/views/CampaignsView.vue'
import CampaignView from '@/views/CampaignView.vue'
import ChatConversationView from '@/views/chat/ChatConversationView.vue'
import ChatView from '@/views/chat/ChatView.vue'
import EditCampaignView from '@/views/EditCampaignView.vue'
import EditListingView from '@/views/EditListingView.vue'
import HomeView from '@/views/home/HomeView.vue'
import ListingView from '@/views/ListingView.vue'
import LoginView from '@/views/LoginView.vue'
import LogoutView from '@/views/LogoutView.vue'
import MyCampaignsView from '@/views/MyCampaignsView.vue'
import MyListingsView from '@/views/MyListingsView.vue'
import NewCampaignView from '@/views/NewCampaignView.vue'
import NewListingView from '@/views/NewListingView.vue'
import NotFound from '@/views/NotFound.vue'
import OnboardingView from '@/views/OnboardingView.vue'
import ProfileView from '@/views/ProfileView.vue'
import RegisterView from '@/views/RegisterView.vue'
import StripeCallbackView from '@/views/StripeCallbackView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        layout: RegisteredUserLayout,
        layoutProps: { fixed: true },
      },
    },
    {
      path: '/prijava',
      name: 'prijava',
      component: LoginView,
      meta: {
        unauthenticatedOnly: true,
      },
    },
    {
      path: '/registracija',
      name: 'registracija',
      component: RegisterView,
      meta: {
        unauthenticatedOnly: true,
      },
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
      meta: {
        layout: RegisteredUserLayout,
      },
    },
    {
      path: '/oglasi/novi',
      name: 'oglasi-novi',
      component: NewListingView,
      meta: {
        layout: RegisteredUserLayout,
      },
    },
    {
      path: '/oglasi/ja',
      name: 'moji-oglasi',
      component: MyListingsView,
      meta: {
        layout: RegisteredUserLayout,
      },
    },
    {
      path: '/oglasi/:id',
      name: 'pregled-oglasa',
      component: ListingView,
      meta: {
        layout: RegisteredUserLayout,
        layoutProps: { width: 'wide' },
      },
    },
    {
      path: '/oglasi/:id/uredi',
      name: 'uredi-oglas',
      component: EditListingView,
      meta: {
        layout: RegisteredUserLayout,
      },
    },
    {
      path: '/donacije',
      name: 'aktivne-donacije',
      component: ActiveDonationsView,
      meta: {
        layout: RegisteredUserLayout,
      },
    },
    {
      path: '/razgovori',
      name: 'razgovori',
      component: ChatView,
      children: [
        {
          path: ':id',
          name: 'aktivan-razgovor',
          component: ChatConversationView,
        },
      ],
      meta: {
        layoutProps: { width: 'full', fixed: true },
        layout: RegisteredUserLayout,
      },
    },
    {
      path: '/stripe-callback',
      name: 'stripe-callback',
      component: StripeCallbackView,
    },
    {
      path: '/kampanje',
      name: 'kampanje',
      component: CampaignsView,
      meta: {
        layout: RegisteredUserLayout,
      },
    },
    {
      path: '/kampanje/ja',
      name: 'moje-kampanje',
      component: MyCampaignsView,
      meta: {
        layout: RegisteredUserLayout,
      },
    },
    {
      path: '/kampanje/nova',
      name: 'nova-kampanja',
      component: NewCampaignView,
      meta: {
        layout: RegisteredUserLayout,
      },
    },
    {
      path: '/kampanje/:id',
      name: 'pregled-kampanje',
      component: CampaignView,
      meta: {
        layout: RegisteredUserLayout,
        layoutProps: { width: 'wide' },
      },
    },
    {
      path: '/kampanje/:id/uredi',
      name: 'uredi-kampanju',
      component: EditCampaignView,
      meta: {
        layout: RegisteredUserLayout,
      },
    },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
  ],
})

export default router
