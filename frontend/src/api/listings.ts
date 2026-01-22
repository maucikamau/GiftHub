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

export async function getListings(
  page: number,
  perPage: number,
  filters?: {
    city?: string
    status?: string
    category?: string
  },
) {
  const searchParams: Record<string, any> = {
    page,
    perPage,
    ...(filters?.city ? { city: filters.city } : {}),
    ...(filters?.status ? { status: filters.status } : {}),
    ...(filters?.category ? { category: filters.category } : {}),
  }

  return await api<PaginatedQuery<Listing> | undefined>('listings/', { searchParams }).json()
}

export async function getActiveListings(page: number, perPage: number) {
  return await api<PaginatedQuery<Listing> | undefined>('listings/active-donations/', { searchParams: { page, perPage } }).json()
}

export async function confirmListingDelivery(listingId: number) {
  return await api(`listings/${listingId}/confirm-delivery/`, {
    method: 'POST',
  }).json()
}

export async function deleteListing(listingId: number) {
  return await api(`listings/${listingId}/`, {
    method: 'DELETE',
  }).json()
}
