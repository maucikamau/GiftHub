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
  deliveryOption: keyof typeof ListingDeliveryOptions
  status: 'pending' | 'accepted' | 'rejected'
  requestId: string
  messageType: 'DonationRequest'
}

export interface ChatPayDeliveryMessage extends BaseChatMessage {
  amount: number
  currency: string
  requestId: string
  messageType: 'PayDelivery'
}

export type ChatMessage = TextChatMessage | ChatDonationRequestMessage | ChatPayDeliveryMessage

declare module 'stream-chat' {
  export interface CustomMessageData {
    messageType?: 'DonationRequest' | 'PayDelivery'
    requestId?: string
    deliveryOption?: keyof typeof ListingDeliveryOptions
    status?: 'pending' | 'accepted' | 'rejected'
    amount?: number
    currency?: string
  }
  export interface CustomUserData {
    internalId?: number
  }
}
