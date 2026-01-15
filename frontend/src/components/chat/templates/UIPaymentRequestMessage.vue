<script setup lang="ts">
import type { ChatPayDeliveryMessage } from '@/types/chat.ts'
import { computed } from 'vue'
import { isChatClientReady } from '@/lib/streamChat.ts'
import { useGetCurrentUser } from '@/services/user.ts'
import { formatCurrency, formatTimestamp } from '@/utils/formatting.ts'

const { message } = defineProps<{
  message: ChatPayDeliveryMessage
}>()

const { data: user } = useGetCurrentUser()

function gotoPayment() {
  // Emit an event to the parent component to handle the status update
  // You can replace this with your actual implementation
  console.log(`Pay`, { pay: message.paymentLink })
  // open in new window the payment link
  window.open(message.paymentLink, '_blank')
}

const isOwn = computed(() => isChatClientReady.value && user.value?.role === 'donor')

const title = computed(() => {
  if (message.status === 'paid')
    return 'Plaćena dostava'

  return isOwn.value ? 'Poslano na plaćanje' : 'Troškovi dostave'
})
</script>

<template>
  <div class="flex gap-3" :class="isOwn ? 'ml-auto' : ''">
    <div
      class="bg-brand-gradient-soft max-w-md min-w-sm w-full rounded-lg p-0.5"
    >
      <div
        class="px-4 py-3 bg-neutral-50 text-neutral-800 rounded-lg"
      >
        <div class="mb-4 mt-2 flex gap-4 items-center">
          <UIcon name="solar:delivery-bold-duotone" class="size-10 shrink-0" />
          <h3 class="font-semibold text-md">
            {{ title }}
          </h3>
        </div>
        <div
          v-if="!isOwn && message.status === 'pending'"
          class="flex gap-4 justify-between rounded-b-lg p-2"
        >
          <div class="w-full text-5xl text-neutral-700">
            {{ formatCurrency(message.amount, message.currency) }}
          </div>
          <div class="shrink-0 grid place-items-center">
            <UButton
              size="md"
              color="primary"
              trailing-icon="i-lucide:arrow-right"
              @click="gotoPayment"
            >
              Plati
            </UButton>
          </div>
        </div>
      </div>
    </div>
    <div class="w-full text-xs flex justify-start items-end text-neutral-500 pb-2">
      {{ formatTimestamp(message.createdAt) }}
    </div>
  </div>
</template>

<style scoped>

</style>
