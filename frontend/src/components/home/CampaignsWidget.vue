<script setup lang="ts">
import { ref } from 'vue'
import { useGetCampaigns } from '@/services/campaigns.ts'

const page = ref(1)
const perPage = ref(50)

const {
  data: campaigns,
  isLoading,
  isError,
} = useGetCampaigns(page, perPage)

</script>

<template>
  <USkeleton v-if="isLoading" class="h-48" />
  <UEmpty
    v-else-if="isError"
    icon="i-tabler-alert-square-rounded"
    title="Pogreška prilikom dohvaćanja"
    description="Došlo je do pogreške prilikom dohvaćanja kampanja. Molimo pokušajte ponovno kasnije."
  />
  <UEmpty
    v-else-if="campaigns?.count === 0"
    icon="i-tabler-alert-square-rounded"
    title="Nema dostupnih kampanja."
    description="Trenutno nema dostupnih kampanja za prikaz."
    :ui="{ body: 'max-w-full' }"
  />
  <div v-else class="flex flex-col gap-2">
    <CampaignCard v-for="campaign in campaigns.results" :key="campaign.id" :campaign="campaign" />
  </div>
</template>
