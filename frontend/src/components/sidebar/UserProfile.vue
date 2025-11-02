<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user.ts'

const items = [
  {
    label: 'Profil',
    to: '/profil',
    icon: 'i-lucide-user',
  },
  {
    label: 'Odjava',
    to: '/prijava',
    icon: 'i-lucide-log-out',
  },
]

const userStore = useUserStore()
const { user } = storeToRefs(userStore)
</script>

<template>
  <UDropdownMenu
    :items="items"
    :ui="{ content: 'w-(--reka-dropdown-menu-trigger-width)' }"
  >
    <UButton variant="ghost" color="neutral" class="text-left px-4 py-2" trailing-icon="i-oui:arrow-up">
      <UUser
        :name="`${user.firstName} ${user.lastName}`"
        :description="user.role.name"
        size="xl"
        class="w-full"
        :avatar="{
          src: 'https://i.pravatar.cc/150?u=jonas',
          icon: 'i-lucide-image',
        }"
      />
    </UButton>
  </UDropdownMenu>
</template>

<style scoped>

</style>
