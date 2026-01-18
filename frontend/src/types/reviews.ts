import type { Listing } from '@/types/listings.ts'

export interface ReviewInput {
  for_listing: number
  rating: number
  comment?: string
}

export interface Review {
  id: number
  donor: number
  reviewer: number
  rating: number
  comment?: string
  listing?: Listing
  created_at: string
}
