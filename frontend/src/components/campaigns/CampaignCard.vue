<script setup lang="ts">
import type { Campaign } from '@/types/campaigns'
import { useRouter } from 'vue-router'
import { computed } from 'vue'
import { can } from '@/lib/permissions.ts'

const props = defineProps<{
  campaign: Campaign
}>()

const { campaign } = props

const router = useRouter()

const progress = computed(() => {
  if (!props.campaign.wish_list?.length) return 0

  const totalNeeded = props.campaign.wish_list.reduce(
    (sum, item) => sum + item.count,
    0
  )

  const totalCollected = props.campaign.wish_list.reduce(
    (sum, item) =>{
      const donatedCount = ('donated' in item) ? (item.donated || 0) : 0
    return sum + donatedCount
  }, 0)

  return totalNeeded > 0
    ? Math.round((totalCollected / totalNeeded) * 100)
    : 0
})
</script>

<template>
  <UCard
    class="bg-transparent hover:bg-neutral-50 transition-colors cursor-pointer"
    variant="soft"
    @click="router.push(`/kampanje/${props.campaign.id}`)"
  >
    <div class="flex gap-6">
      <div class="h-full w-60 flex-shrink-0">
        <AppImage
          :src="campaign.picture ? campaign.picture : ''"
          :alt="campaign.title"
          class="h-full"
          fallback-text="Nema slike"
        />
      </div>
      <div class="flex-1 flex flex-col">
        <div class="flex gap-4 items-end">
          <h3 class="font-bold text-2xl text-stone-900">
            {{ campaign.title }}
          </h3>
          <h4 class="font-medium text-md text-stone-700">
            {{ campaign.location }}
          </h4>
        </div>
        <div class="mt-2 max-w-sm">
          <UProgress v-model="progress" size="sm" color="success" />
          <p v-if="progress < 100" class="text-sm text-black mt-1">
            {{ progress }}% riješeno
          </p>
          <p v-else class="text-sm text-black mt-1">
            Kampanja je uspješno riješena 🎉
          </p>
        </div>
        <p class="text-md font-medium break-all max-h-20 mr-16 overflow-hidden text-stone-700 my-2 h-20">
          {{ campaign.description.length > 150 ? `${campaign.description.substring(0, 150)}...` : campaign.description }}
        </p>
        <!-- <div class="flex flex-wrap gap-2 mt-auto">
          <UBadge v-for="(item, index) in campaign.wish_list" :key="index" color="gray" variant="subtle" class="px-2">
            {{ item.name }} <span class="ml-1 font-bold">{{ donationStore.getDonationCount(campaign.id, item.name) }}/{{ item.count }}</span>
          </UBadge>
        </div> -->
      </div>
      <div class="flex-shrink-0">
        <UButton
          v-if="can('campaigns.change_campaign')"
          :ui="{ base: 'px-4 py-2 text-base', leadingIcon: 'size-6' }"
          variant="outline"
          color="primary"
          icon="i-lucide:pencil"
          :to="`/kampanje/${campaign.id}/uredi`"
          @click.stop="() => void 0"
        >
          Uredi kampanju
        </UButton>
      </div>
    </div>
  </UCard>
</template>
