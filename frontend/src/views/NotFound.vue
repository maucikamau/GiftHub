<script setup lang="ts">
import CardLayout from '@/layouts/CardLayout.vue'
</script>

<template>
  <CardLayout>
    <div class="grid place-items-center h-full">
      <UCard variant="outline" class="px-8 py-4 shadow-md text-center m-4 w-full max-w-md">
        <h1 class="text-9xl font-extrabold text-neutral-600">
          404
        </h1>
        <p class="text-2xl font-medium mt-4">
          Stranica ne postoji
        </p>
        <p class="mt-2 text-neutral-400">
          Stranica kojoj pokušavate pristupiti ne postoji ili je premještena.
        </p>
        <UButton
          to="/" class="mt-6" icon="i-iconamoon:home-duotone" color="primary"
          variant="soft" size="xl"
        >
          Idi na početnu stranicu
        </UButton>
      </UCard>
    </div>
  </CardLayout>
</template>
