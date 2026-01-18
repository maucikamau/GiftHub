import type { App, InjectionKey, Plugin, Ref } from 'vue'
import type { ChatConversation } from '@/types/chat.ts'
import { StreamChat } from 'stream-chat'
import { effectScope, ref, watch } from 'vue'
import { api } from '@/lib/apiClient.ts'
import { useGetCurrentUser } from '@/services/user.ts'
import { cached, invalidateSessionCache } from '@/utils/cache.ts'

const apiKey = window.STREAM_CHAT_API_KEY || import.meta.env.VITE_STREAM_CHAT_API_KEY
export const chatClient = StreamChat.getInstance(apiKey)

export const isChatClientReady = ref(false)

function prepare(app: App, fn: () => void) {
  app.runWithContext(() => {
    const scope = effectScope(true)
    scope.run(fn)
    app.onUnmount(() => scope.stop(true))
  })
}

async function getChatToken(uid: string) {
  return cached(`token_${uid}`, async () => {
    return await api.post<{ token: string }>('chat/').json().then(data => data.token)
  })
}

export const chatPlugin: Plugin = {
  install: (app: App) => prepare(app, () => {
    const { data: user } = useGetCurrentUser()
    watch(user, (user) => {
      if (!user) {
        chatClient.disconnectUser()
        isChatClientReady.value = false

        return
      }

      chatClient.connectUser({ id: user.chat_uid!, internalId: user.id! }, () => getChatToken(user.chat_uid!))
        .catch((err) => {
          console.error('Failed to connect chat user', err)
          invalidateSessionCache('token')
        })
    }, { immediate: true })
  }),
}

chatClient.on('connection.changed', (event) => {
  isChatClientReady.value = event.online ?? false
})

export const CurrentChatConversationKey = Symbol('CurrentChatConversation') as InjectionKey<Ref<ChatConversation | null>>
