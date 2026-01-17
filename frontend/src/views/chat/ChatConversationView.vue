<script setup lang="ts">
import type { ChatConversation, ChatMessage } from '@/types/chat.ts'
import { computed, h, provide, ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import UIChatTextMessage from '@/components/chat/templates/UIChatTextMessage.vue'
import UIDonationRequestMessage from '@/components/chat/templates/UIDonationRequestMessage.vue'
import UIPaymentRequestMessage from '@/components/chat/templates/UIPaymentRequestMessage.vue'
import { useStreamChatChannel } from '@/lib/chat/useStreamChatChannel.ts'
import { CurrentChatConversationKey } from '@/lib/streamChat.ts'
import { useGetListing } from '@/services/listings.ts'

const route = useRoute('aktivan-razgovor')
const activeConversationId = computed(() => route.params.id as string)

const { messages, channel, receiver } = useStreamChatChannel(activeConversationId)
const { data: listing } = useGetListing(() => channel.value?.data?.listingId)
const activeConversation = ref<ChatConversation | null>(null)

watchEffect(() => {
  if (!channel.value || !listing.value || !activeConversationId.value || !receiver.value) {
    activeConversation.value = null
    return
  }

  activeConversation.value = {
    id: activeConversationId.value,
    listing: listing.value,
    receiver: receiver.value,
  }
})

provide(CurrentChatConversationKey, activeConversation)

function ChatMessageWrapper(props: { message: ChatMessage }) {
  if (props.message.deletedAt)
    return h('div', { class: 'text-center text-sm italic text-neutral-500 my-2' }, 'Ova je poruka izbrisana.')
  if ('messageType' in props.message) {
    if (props.message.messageType === 'DonationRequest')
      return h(UIDonationRequestMessage, { message: props.message })
    else if (props.message.messageType === 'PaymentRequest')
      return h(UIPaymentRequestMessage, { message: props.message })
  }

  return h(UIChatTextMessage, { message: props.message })
}
</script>

<template>
  <div v-if="activeConversation && receiver" class="flex flex-col gap-4">
    <div class="flex justify-between">
      <UUser
        :name="receiver.username"
        :avatar="{ src: receiver.avatar }"
        :chip="{
          color: receiver.online ? 'success' : 'surface',
          position: 'top-right',
        }"
        :ui="{
          root: 'gap-4',
          name: 'text-3xl font-bold text-neutral-900',
          avatar: 'size-12',
          description: 'text-md text-neutral-600',
        }"
      >
        <template #description>
          <UButton
            variant="ghost"
            color="surface"
            size="sm"
            trailing-icon="i-oui:arrow-right"
            class="-ml-2"
            :to="{ name: 'pregled-oglasa', params: { id: activeConversation.listing.id } }"
          >
            {{ activeConversation.listing.title }}
          </UButton>
        </template>
      </UUser>
    </div>
    <div class="flex-1 mt-4">
      <!-- Chat area -->
      <UChatMessages>
        <ChatMessageWrapper
          v-for="(message, index) in messages"
          :key="index"
          :message="message"
        />
      </UChatMessages>
    </div>
    <ChatMessageComposer :channel="channel" />
  </div>
</template>
