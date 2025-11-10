<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { UserRoles } from '@/services/user.ts'
import { useUserStore } from '@/stores/user.ts'

const items = [
  {
    label: 'Profil',
    to: '/profil',
    icon: 'i-lucide-user',
  },
  {
    label: 'Odjava',
    to: '/odjava',
    icon: 'i-lucide-log-out',
  },
]

const userStore = useUserStore()
const { user } = storeToRefs(userStore)
</script>

<template>
  <UDropdownMenu
    v-if="user"
    :items="items"
    :ui="{ content: 'w-(--reka-dropdown-menu-trigger-width)' }"
  >
    <UButton variant="ghost" color="neutral" class="text-left px-4 py-2" trailing-icon="i-oui:arrow-up">
      <UUser
        :name="`${user.first_name} ${user.last_name}`"
        :description="user.role ? UserRoles[user.role] : 'Korisnik'"
        size="xl"
        class="w-full"
        :ui="{ name: 'font-semibold' }"
      />
    </UButton>
  </UDropdownMenu>
</template>

<style scoped>

</style>
