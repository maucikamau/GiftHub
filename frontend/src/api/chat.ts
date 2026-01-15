import type { ListingDeliveryOptions } from '@/schemas/listings.ts'
import type { GenericAPIResponse } from '@/types/auth.ts'
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
