<script setup lang="ts">
import type { ChatConversationModel } from '@/lib/streamChat.ts'
import type { ListingDeliveryOptions } from '@/schemas/listings.ts'
import { ref } from 'vue'
import { createDeliveryRequest } from '@/api/chat.ts'

const { forConversation } = defineProps<{
  forConversation: ChatConversationModel
}>()

const emit = defineEmits<{
  (e: 'close', success: boolean): void
}>()

const deliveryOptions = [
  {
    label: 'Osobno preuzimanje',
    description: 'Preuzimate igračku osobno na dogovorenoj lokaciji s oglašivačem, bez dodatnih troškova.',
    value: 'pickup',
  },
  {
    label: 'Dostava o trošku primatelja',
    description: 'Zatražite dostavu na Vašu adresu. Snosite troškove dostave, a troškove će obračunati oglašivač na temelju procjene dostavljača.',
    value: 'shipping',
  },
]

const selectedDeliveryOption = ref<keyof typeof ListingDeliveryOptions>()

async function sendMessage() {
  if (!selectedDeliveryOption.value)
    return

  createDeliveryRequest(forConversation.listing.id, selectedDeliveryOption.value)
    .then(() => {
      emit('close', true)
    })
    .catch((err) => {
      console.error('Error sending donation request:', err)
      emit('close', false)
    })
}
</script>

<template>
  <UModal title="Pošalji zahtjev za donacijom">
    <template #body>
      <URadioGroup v-model="selectedDeliveryOption" variant="card" :items="deliveryOptions" size="xl" />
    </template>
    <template #footer="{ close }">
      <UButton
        icon="i-lucide:hand-heart"
        label="Pošalji zahtjev"
        :disabled="!selectedDeliveryOption"
        :variant="selectedDeliveryOption ? 'solid' : 'soft'"
        color="primary"
        @click="sendMessage"
      />
      <UButton label="Otkaži" color="neutral" variant="ghost" @click="close" />
    </template>
  </UModal>
</template>

<style scoped>

</style>
