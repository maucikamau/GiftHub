import type { Listing, ListingInput } from '@/types/listings.ts'
import { api } from '@/lib/apiClient.ts'
import { objectToFormData } from '@/utils/form.ts'

export async function getMyListings() {
  return await api<Listing[] | undefined>('listings/me/').json()
}

export async function createListing(listing: ListingInput) {
  return await api<Listing>('listings/', {
    method: 'POST',
    body: objectToFormData(listing),
  }).json()
}

export async function getListing(id: number) {
  return await api<Listing>(`listings/${id}/`).json()
}
