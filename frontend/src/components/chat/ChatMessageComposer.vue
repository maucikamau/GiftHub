<script setup lang="ts">
import type { Channel } from 'stream-chat'
import { computed, inject, ref } from 'vue'
import { chatClient } from '@/lib/streamChat.ts'
import { useGetCurrentUser } from '@/services/user.ts'
import { CurrentChatConversationKey } from '@/types/chat.ts'
import { useModal } from '@/utils/modal.ts'

const { channel } = defineProps<{
  channel: Channel | undefined
}>()

const { data: user } = useGetCurrentUser()

const messageContent = ref('')
const readyToSend = computed(() => messageContent.value?.trim().length > 0)
const { showDonationRequestModal, showPaymentRequestDialog } = useModal()
const activeConversation = inject(CurrentChatConversationKey)!

const listingOwnerMember = computed(() => {
  if (!channel)
    return null

  // TODO: Get from custom data
  return Object.values(channel.state.members).find(m => m.user_id === activeConversation.value?.listing.owner.chat_uid) || null
})

const canSendRequest = computed(() => {
  if (!user || !channel)
    return false

  if (!listingOwnerMember.value)
    return false

  if (channel.data?.delivery_accepted)
    return false

  return listingOwnerMember.value.user_id !== chatClient.userID
})

const canRequestPay = computed(() => {
  if (!user || !channel)
    return false

  if (!listingOwnerMember.value)
    return false

  if (!channel.data?.delivery_accepted)
    return false

  return listingOwnerMember.value.user_id === chatClient.userID
})

async function sendMessage(ev?: KeyboardEvent) {
  if (ev && ev.shiftKey)
    return

  ev?.preventDefault()

  if (!readyToSend.value)
    return

  // Logic to send the message
  console.log('Sending message:', messageContent.value)

  const res = await channel?.sendMessage({
    text: messageContent.value,
  }).catch((err) => {
    console.error('Error sending message:', err)
    return false
  })
  messageContent.value = ''

  if (!res)
    return
}
</script>

<template>
  <div
    v-if="channel && activeConversation"
    class="bg-surface-200 pl-3 rounded-xl gap-1 flex flex-col"
  >
    <UTextarea
      v-model="messageContent"
      autoresize
      class="flex-1 h-full px-2 py-3"
      :rows="1"
      :maxrows="4"
      variant="none"
      placeholder="Napišite poruku..."
      @keydown.enter="sendMessage"
    />
    <div class="flex shrink-0 justify-end pr-3 gap-1 mb-3">
      <UTooltip v-if="canSendRequest" text="Pošalji zahtjev" :delay-duration="10" :content="{ side: 'top' }">
        <UButton
          icon="i-lucide:hand-heart"
          color="surface"
          class="rounded-full"
          size="xl"
          variant="ghost"
          @click="showDonationRequestModal(activeConversation)"
        >
          Zahtjev
        </UButton>
      </UTooltip>
      <UTooltip v-if="canRequestPay" text="Zatraži uplatu" :delay-duration="10" :content="{ side: 'top' }">
        <UButton
          icon="i-si:money-fill"
          color="surface"
          class="rounded-full"
          size="xl"
          variant="ghost"
          @click="showPaymentRequestDialog(activeConversation)"
        >
          Naplati dostavu
        </UButton>
      </UTooltip>
      <UButton
        icon="i-lets-icons:send-duotone"
        color="surface"
        class="rounded-full"
        :disabled="!readyToSend"
        :ui="{
          leadingIcon: 'size-7',
        }"
        :variant="readyToSend ? 'solid' : 'soft'"
        size="md"
        @click="sendMessage()"
      />
    </div>
  </div>
</template>

<style scoped />
