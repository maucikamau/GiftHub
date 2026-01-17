<script setup lang="ts">
import type { CampaignInput } from '@/types/campaigns.ts'
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useGetCampaign, useUpdateCampaign } from '@/services/campaigns.ts'

const route = useRoute('uredi-kampanju')
const router = useRouter()

const {
  data: campaign,
  isLoading,
} = useGetCampaign(() => Number(route.params.id))

const { mutateAsync: updateCampaign } = useUpdateCampaign()

const campaignInput = ref<Partial<CampaignInput>>()

async function publish(data: Partial<CampaignInput>) {
  const updatedCampaign = { ...data, id: Number(route.params.id) } as CampaignInput & { id: number }

  await updateCampaign(updatedCampaign, {
    async onSuccess() {
      await router.push({ name: 'pregled-kampanje', params: { id: Number(route.params.id) } })
    },
  })
}

watch(campaign, async (newCampaign) => {
  if (!newCampaign)
    return

  const picture = newCampaign.picture
    ? await fetch(newCampaign.picture)
        .then(res => res.blob())
        .then((blob) => {
          const filename = newCampaign.picture?.split('/').pop() || 'image.jpg'
          return new File([blob], filename, { type: blob.type })
        })
        .catch(() => undefined)
    : undefined

  campaignInput.value = { ...newCampaign, picture, location: newCampaign.location.id }
}, { immediate: true })
</script>

<template>
  <p class="text-sm mb-6">
    Kampanje / <span class="text-primary-600">Uredi kampanju</span>
  </p>
  <USkeleton v-if="isLoading" class="w-full h-96" />
  <CampaignForm v-else-if="campaignInput" v-model="campaignInput" @publish="publish" />
</template>
