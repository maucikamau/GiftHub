<script setup lang="ts">
import { OverlayScrollbarsComponent } from 'overlayscrollbars-vue'
import Logo from '@/assets/PlayForward_Logo.svg'
import SidebarNavigation from '@/components/sidebar/SidebarNavigation.vue'

const { width = 'normal', fixed = false } = defineProps<{
  width?: 'normal' | 'wide' | 'full'
  fixed?: boolean
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
    name: 'Kampanje',
    icon: 'i-solar:gift-bold',
    to: '/kampanje',
    permission: 'campaigns.can_view',
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
  {
    name: 'Moje kampanje',
    icon: 'i-solar:gift-bold',
    to: '/kampanje/ja',
    permission: 'campaigns.add_campaign',
  },
]
</script>

<template>
  <div class="h-screen flex bg-surface-bg">
    <div class="w-80 shrink-0 p-4 flex flex-col">
      <img :src="Logo" class="text-6xl w-7/8 mt-2 mb-4">
      <SidebarNavigation :items="navigationItems" />
      <div class="flex-1" />
      <UserProfile />
    </div>
    <div class="bg-brand-gradient-soft w-full rounded-lg m-2 p-0.5">
      <OverlayScrollbarsComponent
        defer
        class="bg-white w-full h-full p-8 rounded-lg overflow-y-auto scrollbar"
      >
        <div
          class="px-4 pb-8" :class="
            [width === 'wide' ? 'max-w-[1400px] mx-auto' : '',
             width === 'full' ? 'w-full mx-auto' : '',
             width === 'normal' ? 'max-w-6xl mx-auto' : '',
             fixed ? 'h-full' : 'min-h-full']"
        >
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
