<script setup lang="ts">
import { OverlayScrollbarsComponent } from 'overlayscrollbars-vue'
import Logo from '@/assets/PlayForward_Logo.svg'
import SidebarNavigation from '@/components/sidebar/SidebarNavigation.vue'

const { wide = false } = defineProps<{
  wide?: boolean
}>()

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
    permission: 'listings.add_listing',
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
  <div class="h-screen flex bg-surface">
    <div class="w-full max-w-[340px] p-2 md:p-4 flex flex-col">
      <img :src="Logo" class="text-6xl h-12 w-min m-3 mb-4">
      <SidebarNavigation :items="navigationItems" />
      <div class="flex-1" />
      <UserProfile />
    </div>
    <div class="bg-brand-gradient-soft w-full rounded-2xl m-4 p-0.5">
      <OverlayScrollbarsComponent
        defer
        class="bg-white w-full h-full p-8 rounded-2xl overflow-y-auto scrollbar"
      >
        <div class="min-h-full px-4 pb-8" :class="wide ? 'max-w-[1400px] mx-auto' : 'max-w-6xl mx-auto'">
          <slot />
        </div>
      </OverlayScrollbarsComponent>
    </div>
  </div>
</template>

<style scoped>
:deep(.scrollbar .os-theme-dark) {
  --os-padding-axis: 32px;
}
</style>
