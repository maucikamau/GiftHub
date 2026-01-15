import type { InjectionKey, Ref } from 'vue'
import type { ChatConversation } from '@/lib/streamChat.ts'
import type { ListingDeliveryOptions } from '@/schemas/listings.ts'
import type { UserOwner } from '@/types/user.ts'

export interface BaseChatMessage {
  id: string
  createdAt: number
  deletedAt: number | null
  from: UserOwner
}

export interface TextChatMessage extends BaseChatMessage {
  content: string
  messageType: 'text'
}

export interface ChatDonationRequestMessage extends BaseChatMessage {
  delivery_type: keyof typeof ListingDeliveryOptions
  status: 'pending' | 'accepted' | 'rejected'
  requestId: string
  messageType: 'DonationRequest'
}

export interface ChatPayDeliveryMessage extends BaseChatMessage {
  amount: number
  currency: string
  requestId: string
  status: 'pending' | 'paid'
  paymentLink: string
  messageType: 'PaymentRequest'
}

export type ChatMessage = TextChatMessage | ChatDonationRequestMessage | ChatPayDeliveryMessage

declare module 'stream-chat' {
  export interface CustomMessageData {
    messageType?: 'DonationRequest' | 'PaymentRequest'
    requestId?: string
    delivery_type?: keyof typeof ListingDeliveryOptions
    status?: 'pending' | 'accepted' | 'rejected'
    payment_url?: string
    amount?: number
    currency?: string
  }
  export interface CustomUserData {
    internalId?: number
  }
}

export const CurrentChatConversationKey = Symbol('CurrentChatConversation') as InjectionKey<Ref<ChatConversation | null>>
