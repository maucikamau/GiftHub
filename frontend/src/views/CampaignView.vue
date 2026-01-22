<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useDeleteCampaign, useGetCampaign } from '@/services/campaigns.ts'
import { useGetCurrentUser } from '@/services/user.ts'
import { useModal } from '@/utils/modal.ts'

const route = useRoute('pregled-kampanje')
const router = useRouter()
const { showDeleteConfirmationModal } = useModal()

const toast = useToast()

const { data: user } = useGetCurrentUser()
const { mutateAsync: deleteCampaign, isPending: isDeleting } = useDeleteCampaign()

const {
  data: campaign,
  isLoading,
  error,
} = useGetCampaign(() => Number(route.params.id))

async function handleDelete() {
  if (!campaign.value)
    return

  const confirmed = await showDeleteConfirmationModal(campaign.value.title, 'campaign')

  if (!confirmed)
    return

  try {
    await deleteCampaign(campaign.value.id)
    toast.add({
      title: 'Kampanja obrisana',
      description: 'Kampanja je uspješno obrisana.',
      color: 'success',
    })
    router.push({ name: 'moje-kampanje' })
  }
  catch (error: any) {
    toast.add({
      title: 'Greška',
      description: error.message || 'Došlo je do greške pri brisanju kampanje.',
      color: 'error',
    })
  }
}
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
    <CampaignPreview :campaign="campaign" mode="view" />
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
        </template>
      </UCard>
      <template
        v-if="campaign.owner.id === user?.id"
      >
        <UButton leading-icon="i-lucide:pencil" size="xl" class="h-12" color="primary" variant="solid" block :to="`/kampanje/${campaign.id}/uredi`">
          Uredi kampanju
        </UButton>
        <UButton
          leading-icon="i-lucide:trash"
          size="xl"
          class="h-12"
          color="error"
          variant="solid"
          block
          :loading="isDeleting"
          @click="handleDelete"
        >
          Obriši kampanju
        </UButton>
      </template>
    </div>
  </div>
</template>
