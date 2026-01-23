import type { ListingDeliveryOptions } from '@/schemas/listings.ts'
import type { ChatDeliveryRequestResponse, CreateChatResponse } from '@/types/chat.ts'
import { api } from '@/lib/apiClient.ts'

export async function createDeliveryRequest(listingId: number, deliveryType: keyof typeof ListingDeliveryOptions) {
  // listing_id

  return await api.post<ChatDeliveryRequestResponse>(
    `chat/delivery/request/${listingId}/`,
    { json: { delivery_type: deliveryType } },
  )
    .json()
    .catch(async (err) => {
      // get response status code and return
      const res = await err.response.json().catch(() => null)
      const exc = new Error(res?.detail || 'Greška prilikom slanja zahtjeva za dostavu.')
      exc.status = res?.status || 500
      throw exc
    })
}

export async function createChat(listingId: number) {
  return await api.post<CreateChatResponse>(
    `chat/create/${listingId}/`,
  )
    .json()
    .catch(async (err) => {
      const res = await err.response.json().catch(() => null)
      const exc = new Error(res?.detail || 'Greška prilikom slanja zahtjeva za dostavu.')
      exc.status = res?.status || 500
      throw exc
    })
}
