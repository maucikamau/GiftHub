<script setup lang="ts">
import { can } from '@/lib/permissions.ts'
import { useRouter } from 'vue-router'
import { useGetMyCampaigns } from '@/services/campaigns.ts'

const {
  data: campaigns,
  isInitialLoading,
  isError,
} = useGetMyCampaigns()

const router = useRouter()

function openCampaign(id: number) {
  router.push({ name: 'pregled-kampanje', params: { id } })
}
</script>

<template>
  <template v-if="can('campaigns.add_campaign')">
    <div class="flex items-center mr-6">
      <h2 class="font-medium text-2xl flex-1 text-neutral-900 mb-4">
        Moje kampanje
      </h2>
      <UButton
        :ui="{ base: 'px-4 py-2 text-base', leadingIcon: 'size-6' }"
        variant="solid"
        color="primary"
        icon="i-lucide:plus"
        to="/kampanje/nova"
        class="mb-4"
      >
        Nova kampanja
      </UButton>
    </div>
    <USkeleton v-if="isInitialLoading" class="h-48" />
    <UEmpty
      v-else-if="isError"
      icon="i-tabler-alert-square-rounded"
      title="Pogreška prilikom dohvaćanja"
      description="Došlo je do pogreške prilikom dohvaćanja vaših kampanja. Molimo pokušajte ponovno kasnije."
    />
    <UEmpty
      v-else-if="campaigns?.length === 0"
      icon="i-tabler-alert-square-rounded"
      title="Još nemate kampanje"
      description="Izradite svoju prvu kampanju."
      :ui="{ body: 'max-w-full' }"
    />
    <div v-else class="flex flex-col gap-2">
      <CampaignCard v-for="campaign in campaigns" :key="campaign.id" :campaign="campaign" @click="openCampaign(campaign.id)" />
    </div>
  </template>
</template>