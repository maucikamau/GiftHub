<script lang="ts" setup>
import type { Listing } from '@/types/listings.ts'
import { computed } from 'vue'
import { ListingConditions, ListingDeliveryOptions } from '@/schemas/listings.ts'

const { listing } = defineProps<{
  listing: Listing
}>()

const listingPicture = computed(() => {
  if ((listing.picture as any) instanceof File) {
    return URL.createObjectURL(listing.picture as unknown as File)
  }

  return listing.picture
})
</script>

<template>
  <div class="flex-1 2xl:max-w-4xl">
    <h2 class="text-4xl font-bold my-4 text-neutral-900">
      {{ listing.title }}
    </h2>
    <div class="flex flex-col lg:flex-row gap-4 justify-between mb-8">
      <h4 class="text-lg font-medium text-neutral-400">
        {{ listing.location }}
      </h4>
      <div class="flex gap-4">
        <h4 class="text-md text-neutral-400">
          {{ ListingConditions[listing.condition] }}
        </h4>
        <h4 class="text-md text-neutral-400">
          {{ listing.category }}
        </h4>
        <h4 class="text-md text-neutral-400">
          {{ ListingDeliveryOptions[listing.delivery] }}
        </h4>
      </div>
    </div>
    <AppImage :src="listingPicture" class="aspect-video w-full shadow-sm" />
    <div class="my-4">
      {{ listing.content }}
    </div>
  </div>
</template>
