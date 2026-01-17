<script setup lang="ts">
import { ref } from 'vue'
import { useGetCampaigns } from '@/services/campaigns.ts'

const page = ref(1)
const perPage = ref(50)

const {
  data: campaigns,
  isLoading,
} = useGetCampaigns(page, perPage)
</script>

<template>
  <USkeleton v-if="isLoading" class="h-48" />
  <div v-else class="flex flex-col gap-2">
    <h2 v-if="campaigns.results.length" class="font-medium text-2xl flex-1 text-neutral-900 mb-4">
      Kampanje
    </h2>
    <CampaignCard v-for="campaign in campaigns.results" :key="campaign.id" :campaign="campaign" />
  </div>
</template>
