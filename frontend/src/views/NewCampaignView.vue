<script setup lang="ts">
import type { CampaignInput } from '@/types/campaigns.ts'
import { useQueryClient } from '@tanstack/vue-query'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { campaignInputSchema } from '@/schemas/campaigns.ts'
import { useCreateCampaign } from '@/services/campaigns.ts'
import { useGetCurrentUser } from '@/services/user.ts'

const router = useRouter()
const { data: user } = useGetCurrentUser()
const qc = useQueryClient()

const campaignInput = ref<Partial<CampaignInput>>({
  title: '',
  description: '',
  location: user.value?.location?.id,
  picture: undefined,
  wish_list: [{ name: '', count: 1, donated: 0 }],
})

const { mutate: publishCampaign, isPending: isPublishing } = useCreateCampaign()
const toast = useToast()

function publish(campaignInput: Partial<CampaignInput>) {
  const campaign = campaignInputSchema.parse(campaignInput)

  publishCampaign(campaign, {
    onSuccess: () => {
      qc.invalidateQueries({
        queryKey: ['campaigns'],
      })
      router.push({ name: 'moje-kampanje' })
      toast.add({
        title: 'Kampanja objavljena',
        description: 'Kampanja je uspješno objavljena.',
        color: 'success',
      })
    },
  })
}
</script>

<template>
  <p class="text-sm mb-6">
    Kampanje / <span class="text-primary-600">Objavi novu kampanju</span>
  </p>
  <CampaignForm v-model="campaignInput" :is-publishing="isPublishing" @publish="publish" />
</template>
