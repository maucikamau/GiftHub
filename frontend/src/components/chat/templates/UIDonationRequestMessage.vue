<script setup lang="ts">
import type { ChatDonationRequestMessage } from '@/types/chat.ts'
import { computed } from 'vue'
import { chatClient, isChatClientReady } from '@/lib/streamChat.ts'
import { ListingDeliveryOptions } from '@/schemas/listings.ts'
import { formatTimestamp } from '@/utils/time.ts'

const { message } = defineProps<{
  message: ChatDonationRequestMessage
}>()

function updateRequestStatus(status: 'accepted' | 'rejected') {
  // Emit an event to the parent component to handle the status update
  // You can replace this with your actual implementation
  console.log(`Donation request ${status} ${message}`)
}

const isOwn = computed(() => isChatClientReady.value && message.from.chat_uid === chatClient.userID)
</script>

<template>
  <div class="px-6 py-4 bg-neutral-50 text-neutral-800 rounded-lg max-w-md w-full" :class="isOwn ? 'ml-auto' : ''">
    <h3 class="font-semibold text-lg">
      {{ isOwn ? 'Poslan zahtjev za donacijom' : 'Zahtjev za donacijom' }}
    </h3>
    <div class="my-4 flex gap-4 items-center">
      <UIcon name="solar:delivery-bold-duotone" class="size-10 shrink-0" />
      <div>
        {{ ListingDeliveryOptions[message.deliveryOption]?.label }}
      </div>
    </div>
    <div v-if="!isOwn" class="bg-neutral-100 -mx-6 -mb-4 rounded-b-lg p-4">
      <div class="flex gap-2 items-center">
        <UButton
          size="sm"
          color="primary"
          class="shrink-0"
          @click="updateRequestStatus('accepted')"
        >
          Prihvati donaciju
        </UButton>
        <UButton
          size="sm"
          color="neutral"
          class="shrink-0"
          @click="updateRequestStatus('rejected')"
        >
          Odbij donaciju
        </UButton>
        <div class="w-full text-xs text-right text-neutral-500 mt-2">
          {{ formatTimestamp(message.createdAt) }}
        </div>
      </div>
    </div>
    <div v-else class="w-full text-xs text-right text-neutral-500 mt-2">
      {{ formatTimestamp(message.createdAt) }}
    </div>
  </div>
</template>

<style scoped>

</style>
