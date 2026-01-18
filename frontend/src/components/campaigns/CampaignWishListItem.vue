<script setup lang="ts">
import type { Campaign } from '@/types/campaigns.ts'
import { useDonateToCampaign } from '@/services/campaigns.ts'

const { campaignId } = defineProps<{
  item: Campaign['wish_list'][number]
  campaignId: number | undefined
  canDonate: boolean
}>()

const { mutate: donate, isPending } = useDonateToCampaign()
const toast = useToast()

function handleDonate(itemName: string) {
  if (!campaignId)
    return

  donate({ itemName, campaignId }, {
    onSuccess: () => {
      toast.add({
        title: 'Hvala vam!',
        description: `Uspješno ste donirali: ${itemName}`,
        color: 'success',
        icon: 'i-heroicons-check-circle',
      })
    },
    onError: (error: any) => {
      toast.add({
        title: 'Greška',
        description: error.message || 'Došlo je do pogreške prilikom donacije.',
        color: 'error',
        icon: 'i-heroicons-x-circle',
      })
    },
  })
}
</script>

<template>
  <div class="bg-gray-50 p-3 rounded-lg border border-gray-100 flex justify-between items-center">
    <span class="font-medium">{{ item.name }}</span>
    <div>
      <UButton
        v-if="canDonate && item.donated < item.count"
        color="primary"
        variant="soft"
        size="lg"
        class="mr-1 py-2 px-4"
        :loading="isPending"
        @click="handleDonate(item.name)"
      >
        Doniraj
      </UButton>
      <UBadge color="primary" variant="soft" size="lg" class="mr-1 py-2 px-4">
        {{ item.donated }}/{{ item.count }}
      </UBadge>
    </div>
  </div>
</template>
