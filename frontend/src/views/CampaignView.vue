<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useGetCampaign } from '@/services/campaigns.ts'
import { useGetCurrentUser } from '@/services/user.ts'
import { useModal } from '@/utils/modal.ts'

const route = useRoute('pregled-kampanje')
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
      <UCard variant="soft" color="primary" class="w-full 2xl:flex-none">
        <template #header>
          <h2 class="font-semibold text-md">
            Objavio
          </h2>
          <UUser
            :name="`@${campaign.owner.username}`"
            size="xl"
            class="w-full my-4"
            :ui="{ name: 'text-2xl font-semibold' }"
          />
          <div class="flex">
            <div class="text-2xl font-medium gap-2 flex items-end">
              <span class="text-6xl">4.5</span>/5
            </div>
            <div class="flex flex-col ml-4">
              <div class="flex items-center gap-1 ml-2">
                <UIcon name="solar:star-bold-duotone" class="size-7 text-yellow-400" />
                <UIcon name="solar:star-bold-duotone" class="size-7 text-yellow-400" />
                <UIcon name="solar:star-bold-duotone" class="size-7 text-yellow-400" />
                <UIcon name="solar:star-bold-duotone" class="size-7 text-yellow-400" />
                <UIcon name="solar:star-bold-duotone" class="size-7 text-neutral-600" />
              </div>
              <UButton variant="ghost" trailing-icon="i-tabler:arrow-right" size="sm" class="mt-1">
                Pogledaj recenzije
              </UButton>
            </div>
          </div>
        </template>
      </UCard>
      <template
        v-if="campaign.owner.id === user?.id"
      >
        <UButton leading-icon="i-lucide:pencil" size="xl" class="h-12" color="primary" variant="solid" block :to="`/kampanje/${campaign.id}/uredi`">
          Uredi kampanju
        </UButton>
        <UButton leading-icon="i-lucide:trash" size="xl" class="h-12" color="error" variant="solid" block @click="showNotImplementedModal()">
          Obriši kampanju
        </UButton>
      </template>
    </div>
  </div>
</template>
