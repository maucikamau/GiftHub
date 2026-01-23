<script setup lang="ts">
import type { Campaign } from '@/types/campaigns.ts'

defineProps<{ campaign: Campaign, isPublishing?: boolean }>()

defineEmits<{
  (e: 'back'): void
  (e: 'confirm'): void
}>()
</script>

<template>
  <div class="flex gap-12">
    <CampaignPreview :campaign="campaign" mode="preview" class="shrink-0" />
    <div class="flex w-[200px] flex-col gap-2 text-center mt-6">
      <UButton block size="xl" color="primary" :disabled="isPublishing" @click="$emit('back')">
        <p>← Natrag</p>
      </UButton>
      <UButton size="xl" block leading-icon="i-tabler-check" color="success" :loading="isPublishing" @click="$emit('confirm')">
        <p>Objavi</p>
      </UButton>
    </div>
  </div>
</template>
