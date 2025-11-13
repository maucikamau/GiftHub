import type { Listing, ListingInput } from '@/types/listings.ts'
import type { PaginatedQuery } from '@/types/pagination.ts'
import { api } from '@/lib/apiClient.ts'
import { objectToFormData } from '@/utils/form.ts'

export async function getMyListings() {
  return await api<Listing[] | undefined>('listings/me/').json()
}

export async function createListing(listing: ListingInput) {
  return await api<Listing>('listings/create/', {
    method: 'POST',
    body: objectToFormData(listing),
  }).json()
}

export async function updateListing(listing: ListingInput & { id: number }) {
  return await api<Listing>(`listings/update/${listing.id}/`, {
    method: 'PATCH',

    body: objectToFormData(listing),
  }).json()
}

export async function getListing(id: number) {
  return await api<Listing>(`listings/${id}/`).json()
}

export async function getListings(page: number, perPage: number) {
  return await api<PaginatedQuery<Listing> | undefined>('listings/', { searchParams: { page, perPage } }).json()
}
