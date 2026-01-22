import type { ListingDeliveryOptions } from '@/schemas/listings.ts'
import type { GenericAPIResponse } from '@/types/auth.ts'
import type { CreateChatResponse } from '@/types/chat.ts'
import { api } from '@/lib/apiClient.ts'

export async function createDeliveryRequest(listingId: number, deliveryType: keyof typeof ListingDeliveryOptions) {
  // listing_id

  return await api.post<GenericAPIResponse>(
    `chat/delivery/request/${listingId}/`,
    { json: { delivery_type: deliveryType } },
  )
    .json()
    .catch((err) => {
      // get response status code and return
      const exc = new Error(err?.response?.detail || 'Greška prilikom slanja zahtjeva za dostavu.')
      exc.status = err?.response?.status || 500
      throw exc
    })
}

export async function createChat(listingId: number) {
  return await api.post<CreateChatResponse>(
    `chat/create/${listingId}/`,
  )
    .json()
    .catch((err) => {
      // get response status code and return
      const exc = new Error(err?.response?.detail || 'Greška prilikom pokretanja razgovora.')
      exc.status = err?.response?.status || 500
      throw exc
    })
}
