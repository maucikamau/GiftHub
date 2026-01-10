<script setup lang="ts">
import type { Campaign } from '@/types/campaigns'
import { can } from '@/lib/permissions.ts'

defineProps<{
  campaign: Campaign
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
          :src="campaign.picture ? campaign.picture : ''"
          :alt="campaign.title"
          class="h-full"
          fallback-text="Nema slike"
        />
      </div>
      <div class="flex-1 flex flex-col">
        <div class="flex gap-4 items-end">
          <h3 class="font-bold text-2xl text-stone-900">
            {{ campaign.title }}
          </h3>
          <h4 class="font-medium text-md text-stone-700">
            {{ campaign.location }}
          </h4>
        </div>
        <p class="text-md font-medium break-all max-h-20 mr-16 overflow-hidden text-stone-700 my-2 h-20">
          {{ campaign.content.length > 150 ? `${campaign.content.substring(0, 150)}...` : campaign.content }}
        </p>
      </div>
      <div class="flex-shrink-0">
        <UButton
          v-if="can('listings.change_listing')"
          :ui="{ base: 'px-4 py-2 text-base', leadingIcon: 'size-6' }"
          variant="outline"
          color="primary"
          icon="i-lucide:pencil"
          :to="`/oglasi/${campaign.id}/uredi`"
          @click.stop="() => void 0"
        >
          Uredi oglas
        </UButton>
      </div>
    </div>
  </UCard>
</template>
