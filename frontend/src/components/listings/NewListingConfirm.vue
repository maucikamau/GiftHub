<script setup lang="ts">
import type { ListingInput } from '@/types/listings.ts'

defineProps<{ listing: ListingInput }>()
</script>

<template>
  <div class="flex gap-12">
    <ListingPreview :listing="listing" class="flex-shrink-0" />
    <div class="flex w-[200px] flex-col gap-2 text-center mt-6">
      <UButton block size="xl" color="primary" @click="$emit('back')">
        <p>← Natrag</p>
      </UButton>
      <UButton size="xl" block leading-icon="i-tabler-check" color="success" @click="$emit('confirm')">
        <p>Objavi</p>
      </UButton>
    </div>
  </div>
</template>
