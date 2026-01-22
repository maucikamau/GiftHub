import type { Review, ReviewInput, ReviewListResponse } from '@/types/reviews.ts'
import { api } from '@/lib/apiClient.ts'

export async function createReview(review: ReviewInput) {
  return await api<Review>('reviews/create', {
    method: 'POST',
    json: review,
  }).json()
}

export async function getUserAvgReviews(userId: number) {
  return await api<{ average: number, stars: number, total: number }>(`reviews/stats/${userId}`).json()
}

export async function getUserReviews(userId: number, page: number = 1, perPage: number = 100) {
  return await api<ReviewListResponse>(`reviews/list/${userId}`, {
    searchParams: { page, perPage },
  }).json()
}
