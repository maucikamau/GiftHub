import { useMutation } from '@tanstack/vue-query'
import { createReview } from '@/api/reviews.ts'

export function useCreateReview() {
  return useMutation({
    mutationFn: createReview,
  })
}
