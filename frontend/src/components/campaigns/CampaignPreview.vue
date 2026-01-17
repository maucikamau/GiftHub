<script lang="ts" setup>
import type { Campaign, CampaignInput } from '@/types/campaigns.ts'
import { computed } from 'vue'
import { useDonateToItem } from '@/services/campaigns'
import { useGetCurrentUser } from '@/services/user.ts'

const props = defineProps<{
  campaign: Campaign | CampaignInput
  mode?: 'preview' | 'view'
}>()

const isPreview = computed(() => props.mode === 'preview')

const toast = useToast()

const { mutate: donate, isPending } = useDonateToItem(() => (props.campaign as Campaign).id)

function handleDonate(itemName: string) {
  donate(itemName, {
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

const { data: user } = useGetCurrentUser()

const campaignPicture = computed(() => {
  if ((props.campaign.picture as any) instanceof File) {
    return URL.createObjectURL(props.campaign.picture as unknown as File)
  }

  return props.campaign.picture
})

const progress = computed(() => {
  if (!props.campaign.wish_list?.length)
    return 0

  const totalNeeded = props.campaign.wish_list.reduce(
    (sum, item) => sum + item.count,
    0,
  )

  if (isPreview.value)
    return 0

  const totalCollected = props.campaign.wish_list.reduce(
    (sum, item) => {
      const donatedCount = ('donated' in item) ? (item.donated || 0) : 0
      return sum + donatedCount
    },
    0,
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
          {{ props.campaign.title }}
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
            {{ props.campaign.location.cityName }}
          </h4>
        </div>
      </div>
    </div>
    <div>
      <div class="flex items-center text-gray-500 space-x-4">
        <i class="i-heroicons-calendar-days-20-solid" />
        <span>
          Završava:
          <strong>
            {{ new Date(props.campaign.end_date).toLocaleDateString('hr-HR', {
              day: '2-digit',
              month: '2-digit',
              year: 'numeric',
            }) }}
          </strong>
        </span>
      </div>
    </div>
    <div class="my-4 break-all p-4">
      {{ props.campaign.description }}
    </div>
    <div v-if="props.campaign.wish_list?.length" class="mt-8 border border-gray-200 rounded-lg p-4">
      <h3 class="text-xl font-bold mb-4">
        Potrebne igračke
      </h3>
      <div class="grid grid-cols-1 sm:grid-cols-1 gap-4 max-h-50 overflow-y-auto pr-2">
        <div v-for="(item, index) in props.campaign.wish_list" :key="index" class="bg-gray-50 p-3 rounded-lg border border-gray-100 flex justify-between items-center">
          <span class="font-medium">{{ item.name }}</span>
          <div>
            <template
              v-if="!isPreview && ('owner' in props.campaign) && props.campaign.owner?.id !== user?.id"
            >
              <UButton
                v-if="(('donated' in item ? item.donated : 0) || 0) < item.count" color="primary" variant="soft" size="lg"
                class="mr-1 py-2 px-4"
                :loading="isPending"
                @click="handleDonate(item.name)"
              >
                Doniraj
              </UButton>
            </template>
            <UBadge color="primary" variant="soft" size="lg" class="mr-1 py-2 px-4">
              {{ item.donated ? item.donated : 0 }}/{{ item.count }}
            </UBadge>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
