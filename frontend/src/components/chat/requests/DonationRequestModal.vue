<script setup lang="ts">
import type { Message } from 'stream-chat'
import type { ChatConversationModel } from '@/lib/streamChat.ts'
import { ref } from 'vue'
import { chatClient } from '@/lib/streamChat.ts'

const { forConversation } = defineProps<{
  forConversation: ChatConversationModel
}>()

const emit = defineEmits<{
  (e: 'close', message: Message): void
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

const selectedDeliveryOption = ref('')

async function sendMessage() {
  if (!selectedDeliveryOption.value)
    return

  console.log('Sending donation request with option:', selectedDeliveryOption.value)

  const channelId = 'id' in forConversation ? forConversation.id : `${forConversation.listing.id}-${chatClient.userID}`
  const channel = chatClient.channel('messaging', channelId, {
    name: forConversation.user.name,
    avatar: forConversation.user.avatar,
    listing: forConversation.listing,
    members: [forConversation.user.chat_uid, chatClient.userID!],
  })
  if (!('id' in forConversation)) {
    await channel.create()
  }
  await channel.sendMessage({
    listing: forConversation.listing,
    messageType: 'DonationRequest',
    deliveryOption: selectedDeliveryOption.value,
  }).then((message) => {
    console.log('Donation request message sent:', message)
    emit('close', message)
  }).catch((error) => {
    console.error('Error sending donation request message:', error)
    emit('close')
  })

  // Check if

  // const textMessage = new CometChat.CustomInteractiveMessage(
  //   selectedUser.getUid(),
  //   CometChat.RECEIVER_TYPE.USER,
  //   'DonationRequestMessage',
  //   {
  //     deliveryOption: selectedDeliveryOption.value,
  //   },
  // )
  // console.log('Sending donation request message:', textMessage)
  // CometChat.sendMessage(textMessage).then(
  //   message => emit('close', message),
  // ).catch(_ => emit('close', null))
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
