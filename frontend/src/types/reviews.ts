import type { Listing } from '@/types/listings.ts'
import type { UserOwner } from '@/types/user.ts'

export interface ReviewInput {
  for_listing: number
  rating: number
  comment?: string
}

export interface Review {
  id: number
  donor: UserOwner
  reviewer: UserOwner
  rating: number
  comment?: string
  listing?: Listing
  created_at: string
}

export interface ReviewListResponse {
  donor: UserOwner
  reviews: Review[]
  count: number
  next: string | null
  previous: string | null
}
