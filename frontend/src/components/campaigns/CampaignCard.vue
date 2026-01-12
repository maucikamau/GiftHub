<script setup lang="ts">
import type { Campaign } from '@/types/campaigns'
import { useRouter } from 'vue-router'
import { can } from '@/lib/permissions.ts'
import { useDonationStore } from '@/stores/donations'

const props = defineProps<{
  campaign: Campaign
}>()

const router = useRouter()
const donationStore = useDonationStore()
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
        <p class="text-md font-medium break-all max-h-20 mr-16 overflow-hidden text-stone-700 my-2 h-20">
          {{ campaign.description.length > 150 ? `${campaign.description.substring(0, 150)}...` : campaign.description }}
        </p>
        <div class="flex flex-wrap gap-2 mt-auto">
          <UBadge v-for="(item, index) in campaign.wish_list" :key="index" color="gray" variant="subtle" class="px-2">
            {{ item.name }} <span class="ml-1 font-bold">{{ donationStore.getDonationCount(campaign.id, item.name) }}/{{ item.count }}</span>
          </UBadge>
        </div>
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
