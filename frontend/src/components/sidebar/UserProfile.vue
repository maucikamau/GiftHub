<script setup lang="ts">
import { useGetCurrentUser, UserRoles } from '@/services/user.ts'

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

const { data: user } = useGetCurrentUser()
</script>

<template>
  <UDropdownMenu
    v-if="user"
    :items="items"
    :ui="{ content: 'w-(--reka-dropdown-menu-trigger-width)' }"
  >
    <UButton variant="ghost" color="surface" class="text-left px-4 py-2" trailing-icon="i-oui:arrow-up">
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
