<script setup lang="ts">
import type { Channel } from 'stream-chat'
import type { ChatConversation } from '@/lib/streamChat.ts'
import type { ChatMessage } from '@/types/chat.ts'
import { h, onMounted, provide, ref, watch } from 'vue'
import UIChatTextMessage from '@/components/chat/templates/UIChatTextMessage.vue'
import UIDonationRequestMessage from '@/components/chat/templates/UIDonationRequestMessage.vue'
import UIPaymentRequestMessage from '@/components/chat/templates/UIPaymentRequestMessage.vue'
import { useStreamChatChannel } from '@/lib/chat/useStreamChatChannel.ts'
import { chatClient } from '@/lib/streamChat.ts'
import { useGetCurrentUser } from '@/services/user.ts'
import { CurrentChatConversationKey } from '@/types/chat.ts'

const activeConversation = ref<ChatConversation | null>(null)
const activeChannel = ref<Channel>()
const { messages } = useStreamChatChannel(activeChannel)
const { data: user } = useGetCurrentUser()

onMounted(async () => {
  if (!chatClient.userID && user.value) {
    // TODO: Handle smarter, this needs to be done with backend support.
    // We need to pull token from backend for security reasons.
    await chatClient.connectUser({
      id: user.value.chat_uid,
      name: user.value.username,
      image: `https://getstream.io/random_svg/?name=${user.value.username}`,
    }, chatClient.devToken(user.value.chat_uid!))
  }
})

watch(activeConversation, async () => {
  if (!activeConversation.value)
    return

  messages.value = []
  activeChannel.value = chatClient.channel('messaging', activeConversation.value.id)
})

provide(CurrentChatConversationKey, activeConversation)

function ChatMessageWrapper(props: { message: ChatMessage }) {
  if (props.message.deletedAt)
    return h('div', { class: 'text-center text-sm italic text-neutral-500 my-2' }, 'Ova je poruka izbrisana.')
  if ('messageType' in props.message) {
    console.log('Rendering special message type:', props.message.messageType)

    if (props.message.messageType === 'DonationRequest')
      return h(UIDonationRequestMessage, { message: props.message })
    else if (props.message.messageType === 'PaymentRequest')
      return h(UIPaymentRequestMessage, { message: props.message })
  }

  return h(UIChatTextMessage, { message: props.message })
}
</script>

<template>
  <div class="flex gap-4 w-full h-full">
    <div class="flex-col">
      <h2 class="font-medium text-2xl flex-1 text-neutral-900 mb-4">
        Nedavni razgovori
      </h2>
      <div class="d-flex flex-col gap-2 w-80">
        <ChatRecents v-model="activeConversation" />
      </div>
    </div>
    <div v-if="activeConversation" class="w-full max-w-[1400px] mx-auto h-full flex flex-col gap-4">
      <div class="flex justify-between">
        <UUser
          :name="activeConversation.user.name"
          :description="activeConversation.listing.title"
          :avatar="{ src: activeConversation.user.avatar }"
          :chip="{
            color: 'primary',
            position: 'top-right',
          }"
          :ui="{
            root: 'gap-4',
            name: 'text-3xl font-bold text-neutral-900',
            avatar: 'size-12',
            description: 'text-md text-neutral-600',
          }"
        />
        <UButton variant="ghost" color="surface" icon="i-lucide:more-vertical" />
      </div>
      <div class="flex-1">
        <!-- Chat area -->
        <UChatMessages>
          <ChatMessageWrapper
            v-for="(message, index) in messages"
            :key="index"
            :message="message"
          />
        </UChatMessages>
      </div>
      <ChatMessageComposer :channel="activeChannel" />
    </div>
  </div>
</template>

<style scoped></style>
