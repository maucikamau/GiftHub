import type { Channel } from 'stream-chat'
import type { Ref } from 'vue'
import type { ChatMessage } from '@/types/chat.ts'
import { ref, toRef, watch } from 'vue'
import { toMessages } from '@/utils/conversation.ts'

export function useStreamChatChannel(channel: Ref<Channel | undefined>) {
  const messages = ref<ChatMessage[]>([])

  const _channel = toRef(channel)

  watch(_channel, (channel, _, onCleanup) => {
    if (!channel)
      return

    channel.watch().then((state) => {
      // TODO: Do conversion properly
      const newMessages = toMessages(state.messages)
      messages.value = newMessages
      console.log('Channel watched, messages loaded', newMessages)
    })
    channel.on('all', (ev) => {
      console.log('Channel event', ev, channel.state)
      messages.value = toMessages(channel.state.messages)
    })

    onCleanup(() => {
      if (!_channel.value)
        return
      _channel.value.stopWatching()
    })
  }, { immediate: true })

  return {
    messages,
  }
}
