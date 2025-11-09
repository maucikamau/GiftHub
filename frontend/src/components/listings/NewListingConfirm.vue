<script setup lang="ts">
import type { ListingInput } from '@/types/listings.ts'

defineProps<{ listing: ListingInput }>()
</script>

<template>
  <div class="flex flex-col">
    <UCard>
      <div class="flex gap-6">
        <div class="w-40">
          <div
            class="w-40 aspect-[16/9] bg-gradient-to-t from-neutral-800 to-neutral-50 rounded-lg"
          />
        </div>
        <div class="flex-1 flex flex-col">
          <div class="flex gap-4 items-end">
            <h3 class="font-bold text-2xl text-stone-900">
              {{ listing.title }}
            </h3>
            <h4 class="font-medium text-md text-stone-700">
              Mjesto
            </h4>
          </div>
          <p class="text-md font-medium text-stone-700 my-2 h-20">
            {{ listing.content }}
          </p>
          <div class="flex gap-4">
            <span class="font-medium text-stone-400">{{ listing.status }}</span>
            <span class="font-medium text-stone-400">{{ listing.category }}</span>
            <span class="font-medium text-stone-400">{{ listing.delivery }}</span>
          </div>
        </div>
      </div>
    </UCard>
    <div class="flex justify-between text-center mt-6">
      <UButton color="primary" @click="$emit('back')">
        <p>← Natrag</p>
      </UButton>
      <UButton leading-icon="i-tabler-check" color="success" @click="$emit('confirm')">
        <p>Objavi</p>
      </UButton>
    </div>
  </div>
</template>
