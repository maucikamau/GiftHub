<script lang="ts" setup>
import type { Campaign, CampaignInput } from '@/types/campaigns.ts'
import { computed } from 'vue'
import { useDonationStore } from '@/stores/donations'
import { useGetCurrentUser } from '@/services/user.ts'

const props = defineProps<{
  campaign: Campaign | CampaignInput
  mode?: 'preview' | 'view'
}>()

const { campaign, mode } = props

const isPreview = computed(() => mode === 'preview')

const donationStore = useDonationStore()

const updateDonationCount = (index: number, delta: number) => {
  const item = campaign.wish_list[index]
  const max = item.count
  const current = donationStore.getDonationCount(campaign.id, item.name)
  const next = current + delta
  if (next >= 0 && next <= max) {
    donationStore.setDonationCount(campaign.id, item.name, next)
  }
}

const { data: user } = useGetCurrentUser()

const campaignPicture = computed(() => {
  if ((campaign.picture as any) instanceof File) {
    return URL.createObjectURL(campaign.picture as unknown as File)
  }

  return campaign.picture
})

const progress = computed(() => {
  if (!campaign.wish_list?.length) return 0

  const totalNeeded = campaign.wish_list.reduce(
    (sum, item) => sum + item.count,
    0
  )

  if (isPreview.value) return 0

  const totalCollected = campaign.wish_list.reduce(
    (sum, item) =>
      sum + donationStore.getDonationCount(campaign.id, item.name),
    0
  )

  return totalNeeded > 0
    ? Math.round((totalCollected / totalNeeded) * 100)
    : 0
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
        <div class="mt-2 max-w-sm">
          <UProgress v-model="progress" size="md" color="success" />
          <p v-if="progress < 100" class="text-sm text-gray-200 mt-1">
            {{ progress }}% riješeno
          </p>
          <p v-else class="text-sm text-white mt-1 font-semibold">
            Kampanja je uspješno riješena 🎉
          </p>
        </div>
        <div class="flex flex-col lg:flex-row gap-4 justify-between">
          <h4 v-if="campaign.location" class="text-lg font-medium text-gray-200">
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
          <div>
            <template
            v-if="!isPreview && campaign.owner && campaign.owner.id !== user?.id"
            >
              <UButton color="primary" variant="soft" size="lg" class="mr-1 py-2 px-4" @click="updateDonationCount(index, 1)">+</UButton>
              <UButton color="primary" variant="soft" size="lg" class="mr-1 py-2 px-4" @click="updateDonationCount(index, -1)">-</UButton>
          </template>
            <UBadge color="primary" variant="soft" size="lg" class="mr-1 py-2 px-4">{{ donationStore.getDonationCount(campaign.id, item.name) }}/{{ item.count }}</UBadge>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
