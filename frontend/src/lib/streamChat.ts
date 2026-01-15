import type { Listing } from '@/types/listings.ts'
import { StreamChat } from 'stream-chat'
import { ref } from 'vue'

const apiKey = window.STREAM_CHAT_API_KEY || import.meta.env.VITE_STREAM_CHAT_API_KEY
export const chatClient = StreamChat.getInstance(apiKey)

export const isChatClientReady = ref(false)

chatClient.on('connection.changed', (event) => {
  isChatClientReady.value = event.online ?? false
  console.log('Chat connection changed', event)
})

export interface TemporaryChatConversation {
  user: {
    id: string
    chat_uid: string
    avatar: string
    name: string
    online?: boolean
  }
  listing: Pick<Listing, 'id' | 'title' | 'picture'>
}

export interface ChatConversation extends TemporaryChatConversation {
  id: string
}

export type ChatConversationModel = TemporaryChatConversation | ChatConversation
