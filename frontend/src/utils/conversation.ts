import type { MessageResponse } from 'stream-chat'
import type {
  ChatDonationRequestMessage,
  ChatMessage,
  ChatPayDeliveryMessage,
  TextChatMessage,
} from '@/types/chat.ts'

export function toMessages(messages: MessageResponse[]): ChatMessage[] {
  return messages.map((msg) => {
    const base = {
      id: msg.id,
      createdAt: new Date(msg.created_at ?? 0).getTime(),
      deletedAt: msg.deleted_at ? new Date(msg.deleted_at).getTime() : null,
      from: {
        id: msg.user?.internalId || 0,
        chat_uid: msg.user?.id || '',
        username: msg.user?.name || 'Nepoznati korisnik',
      },
    }
    if (msg.messageType === 'DonationRequest') {
      return {
        ...base,
        messageType: 'DonationRequest',
        requestId: msg.requestId || '',
        delivery_type: msg.delivery_type || 'pickup',
        status: msg.donation_status || 'pending',
      } satisfies ChatDonationRequestMessage
    }
    else if (msg.messageType === 'PaymentRequest') {
      return {
        ...base,
        messageType: 'PaymentRequest',
        requestId: msg.requestId || '',
        amount: msg.amount || 0,
        currency: msg.currency || 'EUR',
        status: 'pending',
        paymentLink: msg.payment_url!,
      } satisfies ChatPayDeliveryMessage
    }

    return { ...base, content: msg.text || '', messageType: 'text' } satisfies TextChatMessage
  })
}
