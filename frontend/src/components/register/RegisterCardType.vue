<script setup lang="ts">
import { useOnboardingStore, UserRole } from '@/stores/onboarding.ts'

const options = [{
  label: 'Donator',
  role: UserRole.DONOR,
  img: '/static/donator.png',
  color: 'secondary',
}, {
  label: 'Primatelj',
  role: UserRole.RECIPIENT,
  img: '/static/primatelj.png',
  color: 'warning',
}]

const store = useOnboardingStore()
</script>

<template>
  <p class="font-medium text-xl my-2 text-left">
    Ja sam...
  </p>
  <div class="flex gap-4 h-40 my-2">
    <UButton
      v-for="option in options"
      :key="option.label"
      class="flex-1 items-end justify-between pr-6 gap-4"
      variant="outline"
      :color="option.color"
      @click="store.chooseRole(option.role)"
    >
      <p class="font-semibold text-lg mb-4">
        {{ option.label }}
      </p>
      <img :src="option.img" class="h-36">
    </UButton>
  </div>
</template>
