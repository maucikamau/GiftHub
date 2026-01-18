import type { Review, ReviewInput } from '@/types/reviews.ts'
import { api } from '@/lib/apiClient.ts'

export async function createReview(review: ReviewInput) {
  return await api<Review>('reviews/create', {
    method: 'POST',
    json: review,
  }).json()
}
