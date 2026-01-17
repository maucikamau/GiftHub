import type { ListingDeliveryOptions } from '@/schemas/listings.ts'
import type { Listing } from '@/types/listings.ts'
import type { UserOwner } from '@/types/user.ts'

declare module 'stream-chat' {
  export interface CustomMessageData {
    messageType?: 'DonationRequest' | 'PaymentRequest'
    requestId?: string
    delivery_type?: keyof typeof ListingDeliveryOptions
    donation_status?: 'pending' | 'accepted' | 'rejected'
    payment_url?: string
    amount?: number
    currency?: string
  }
  export interface CustomChannelData {
    listingId?: number
    delivery_accepted?: boolean
  }
  export interface CustomUserData {
    internalId: number
    avatar?: string
  }
}

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

export interface CreateChatResponse {
  id: string
  stream_channel_id: string
  listing_id: number
}

export type ChatConversationReceiver = UserOwner & { online?: boolean }
export interface TemporaryChatConversation {
  receiver: ChatConversationReceiver
  listing: Pick<Listing, 'id' | 'title' | 'picture'>
}

export interface ChatConversation extends TemporaryChatConversation {
  id: string
  listing: Listing
}

export type ChatConversationModel = TemporaryChatConversation | ChatConversation
