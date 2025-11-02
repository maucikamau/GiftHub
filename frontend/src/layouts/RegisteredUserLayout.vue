<script setup lang="ts">
import Logo from '@/assets/PlayForward_Logo.svg'
import SidebarNavigation from '@/components/sidebar/SidebarNavigation.vue'

const navigationItems = [
  { name: 'Početna', icon: 'i-iconamoon:home-duotone', to: '/' },
  {
    name: 'Aktivne donacije',
    icon: 'i-solar:cart-bold-duotone',
    to: '/donacije',
    permission: 'donations.can_view_active',
  },
  {
    name: 'Moji oglasi',
    icon: 'i-ph:cards-three-duotone',
    to: '/oglasi/ja',
    permission: 'ads.can_view_own',
  },
  {
    name: 'Razgovori',
    icon: 'i-solar:chat-round-line-bold-duotone',
    to: '/razgovori',
    permission: 'chat.can_access',
  },
]
</script>

<template>
  <div class="min-h-screen flex bg-surface">
    <div class="w-full max-w-[340px] p-2 md:p-4 flex flex-col">
      <img :src="Logo" class="text-6xl h-12 w-min m-3 mb-4">
      <SidebarNavigation :items="navigationItems" />
      <div class="flex-1" />
      <UserProfile />
    </div>
    <div class="bg-brand-gradient-soft w-full rounded-2xl m-4 p-0.5">
      <div class="bg-white w-full h-full p-8 rounded-2xl">
        <div class="w-full h-full mx-auto max-w-6xl px-4 overflow-y-auto">
          <slot />
        </div>
      </div>
    </div>
  </div>
</template>
