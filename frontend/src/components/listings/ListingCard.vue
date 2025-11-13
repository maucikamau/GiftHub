<script setup lang="ts">
import type { Listing } from '@/types/listings'
import { can } from '@/lib/permissions.ts'
import { ListingConditions, ListingDeliveryOptions } from '@/schemas/listings.ts'

defineProps<{
  listing: Listing
}>()
</script>

<template>
  <UCard
    class="bg-transparent hover:bg-neutral-50 transition-colors cursor-pointer"
    variant="soft"
  >
    <div class="flex gap-6">
      <div class="h-full w-60 flex-shrink-0">
        <AppImage
          :src="listing.picture ? listing.picture : ''"
          :alt="listing.title"
          class="h-full"
          fallback-text="Nema slike"
        />
      </div>
      <div class="flex-1 flex flex-col">
        <div class="flex gap-4 items-end">
          <h3 class="font-bold text-2xl text-stone-900">
            {{ listing.title }}
          </h3>
          <h4 class="font-medium text-md text-stone-700">
            {{ listing.location }}
          </h4>
        </div>
        <p class="text-md font-medium break-all max-h-20 mr-16 overflow-hidden text-stone-700 my-2 h-20">
          {{ listing.content.length > 150 ? `${listing.content.substring(0, 150)}...` : listing.content }}
        </p>
        <div class="flex gap-4">
          <span class="font-medium text-stone-400">{{ ListingConditions[listing.condition] }}</span>
          <span class="font-medium text-stone-400">{{ listing.category }}</span>
          <span class="font-medium text-stone-400">{{ ListingDeliveryOptions[listing.delivery] }}</span>
        </div>
      </div>
      <div class="flex-shrink-0">
        <UButton
          v-if="can('listings.change_listing')"
          :ui="{ base: 'px-4 py-2 text-base', leadingIcon: 'size-6' }"
          variant="outline"
          color="primary"
          icon="i-lucide:pencil"
          :to="`/oglasi/${listing.id}/uredi`"
          @click.stop="() => void 0"
        >
          Uredi oglas
        </UButton>
      </div>
    </div>
  </UCard>
</template>
