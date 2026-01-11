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
    <h2 class="text-4xl font-bold my-4 text-neutral-900">
      {{ campaign.title }}
    </h2>
    <div class="flex flex-col lg:flex-row gap-4 justify-between mb-8">
      <h4 class="text-lg font-medium text-neutral-400">
        {{ campaign.location.cityName }}
      </h4>
    </div>
    <AppImage :src="campaignPicture" class="aspect-video w-full shadow-sm" />
    <div class="my-4 break-all">
      {{ campaign.description }}
    </div>
    <div v-if="campaign.wish_list?.length" class="mt-8">
      <h3 class="text-xl font-bold mb-4">Potrebne igračke</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div v-for="(item, index) in campaign.wish_list" :key="index" class="bg-gray-50 p-3 rounded-lg border border-gray-100 flex justify-between items-center">
          <span class="font-medium">{{ item.name }}</span>
          <UBadge color="primary" variant="soft" size="lg">{{ item.count }}</UBadge>
        </div>
      </div>
    </div>
  </div>
</template>
