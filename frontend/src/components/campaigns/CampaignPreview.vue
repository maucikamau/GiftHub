<script lang="ts" setup>
import type { Campaign } from '@/types/campaigns.ts'
import { computed } from 'vue'

const { campaign } = defineProps<{
  campaign: Campaign
}>()

const campaignPicture = computed(() => {
  if ((campaign.picture as any) instanceof File) {
    return URL.createObjectURL(campaign.picture as unknown as File)
  }

  return campaign.picture
})
</script>

<template>
  <div class="flex-1 2xl:max-w-4xl">
    <div class="relative overflow-hidden rounded-xl shadow-sm mb-4">
      <AppImage :src="campaignPicture" class="aspect-video w-full max-h-70 brightness-50" />
      <div class="absolute inset-0 flex flex-col justify-end p-6">
        <h2 class="text-4xl font-bold mb-2 text-white">
          {{ campaign.title }}
        </h2>
        <div class="flex flex-col lg:flex-row gap-4 justify-between">
          <h4 class="text-lg font-medium text-gray-200">
            {{ campaign.location.cityName }}
          </h4>
        </div>
      </div>
    </div>
    <div class="my-4 break-all p-4">
      {{ campaign.description }}
    </div>
    <div v-if="campaign.wish_list?.length" class="mt-8 border border-gray-200 rounded-lg p-4">
      <h3 class="text-xl font-bold mb-4">Potrebne igračke</h3>
      <div class="grid grid-cols-1 sm:grid-cols-1 gap-4 max-h-50 overflow-y-auto pr-2">
        <div v-for="(item, index) in campaign.wish_list" :key="index" class="bg-gray-50 p-3 rounded-lg border border-gray-100 flex justify-between items-center">
          <span class="font-medium">{{ item.name }}</span>
          <UBadge color="primary" variant="soft" size="lg">{{ item.count }}</UBadge>
        </div>
      </div>
    </div>
  </div>
</template>
