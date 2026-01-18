import type { Channel, MessageResponse } from 'stream-chat'
import type { MaybeRefOrGetter } from 'vue'
import type { ChatConversationReceiver, ChatMessage } from '@/types/chat.ts'
import { ref, shallowRef, toRef, watch } from 'vue'
import { chatClient } from '@/lib/streamChat.ts'
import { toMessages } from '@/utils/conversation.ts'

function getReceiverFromChannel(channel: Channel): ChatConversationReceiver | undefined {
  const _receiver = Object.values(channel.state.members).find(
    member => member.user_id !== chatClient.userID,
  )
  if (_receiver && _receiver.user) {
    return {
      id: _receiver.user.internalId,
      chat_uid: _receiver.user.id,
      username: _receiver.user.name!,
      online: _receiver.user.online,
    }
  }
  return undefined
}

export function useStreamChatChannel(channelId: MaybeRefOrGetter<string | undefined>) {
  const messages = ref<ChatMessage[]>([])

  const _channelId = toRef(channelId)
  const trackedChannel = shallowRef<Channel>()
  const receiver = ref<ChatConversationReceiver>()

  watch(_channelId, async (channelId, _, onCleanup) => {
    if (!channelId)
      return

    const channel = chatClient.channel('messaging', channelId)
    const state = await channel.watch({ presence: true })
    trackedChannel.value = channel
    messages.value = toMessages(state.messages)

    receiver.value = getReceiverFromChannel(channel)

    const { unsubscribe } = channel.on('all', (ev) => {
      console.log('Channel event', ev, channel.state)
      messages.value = toMessages(channel.state.messages as any as MessageResponse[])

      receiver.value = getReceiverFromChannel(channel)
    })

    onCleanup(() => {
      unsubscribe()

      if (!trackedChannel.value)
        return
      trackedChannel.value.stopWatching()
    })
  }, { immediate: true })

  return {
    messages,
    receiver,
    channel: trackedChannel,
  }
}
