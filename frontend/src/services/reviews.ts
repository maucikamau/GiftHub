import type { MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery } from '@tanstack/vue-query'
import { computed, toValue } from 'vue'
import { createReview, getUserAvgReviews, getUserReviews } from '@/api/reviews.ts'

export function useCreateReview() {
  return useMutation({
    mutationFn: createReview,
  })
}

export function useGetUserAvgReviews(userId: MaybeRefOrGetter<number | undefined>) {
  return useQuery({
    queryKey: computed(() => (['reviews', 'average', toValue(userId)])),
    enabled: computed(() => !!toValue(userId)),
    queryFn: async () => getUserAvgReviews(toValue(userId)!),
  })
}

export function useGetUserReviews(userId: MaybeRefOrGetter<number | undefined>, page: MaybeRefOrGetter<number> = 1, perPage: MaybeRefOrGetter<number> = 100) {
  return useQuery({
    queryKey: computed(() => (['reviews', 'list', toValue(userId), toValue(page), toValue(perPage)])),
    enabled: computed(() => !!toValue(userId)),
    queryFn: async () => getUserReviews(toValue(userId)!, toValue(page), toValue(perPage)),
  })
}
