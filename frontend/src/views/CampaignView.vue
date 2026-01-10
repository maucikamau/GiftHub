<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useGetCampaign } from '@/services/campaigns.ts'
import { useGetCurrentUser } from '@/services/user.ts'
import { useModal } from '@/utils/modal.ts'

const route = useRoute('pregled-oglasa')
const { data: user } = useGetCurrentUser()

const { showNotImplementedModal } = useModal()

const {
  data: campaign,
  isLoading,
  error,
} = useGetCampaign(() => Number(route.params.id))
</script>

<template>
  <USkeleton v-if="isLoading" class="w-full h-40" />
  <UEmpty
    v-if="error && error.message.includes('404')"
    title="Kampanja nije pronađena"
    description="Kampanja koju tražite ne postoji ili je uklonjena."
    icon="i-tabler:search-off"
  />
  <div v-else-if="campaign" class="flex flex-col 2xl:flex-row justify-between gap-20">
    <CampaignPreview :campaign="campaign" />
    <div class="2xl:w-sm flex flex-col gap-4">
      <template
        v-if="campaign.owner.id === user?.id"
      >
        <UButton leading-icon="i-lucide:pencil" size="xl" class="h-12" color="primary" variant="solid" block :to="`/oglasi/${campaign.id}/uredi`">
          Uredi kampanju
        </UButton>
        <UButton leading-icon="i-lucide:trash" size="xl" class="h-12" color="error" variant="solid" block @click="showNotImplementedModal()">
          Obriši kampanju
        </UButton>
      </template>
    </div>
  </div>
</template>
