import type { MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery } from '@tanstack/vue-query'
import { computed, toValue } from 'vue'
import { createListing, getListing, getMyListings } from '@/api/listings.ts'

export function useGetMyListings() {
  return useQuery({
    queryKey: ['listings', 'me'],
    queryFn: getMyListings,
  })
}

export function useCreateListing() {
  return useMutation({
    mutationFn: createListing,
  })
}

export function useGetListing(id: MaybeRefOrGetter<number>) {
  return useQuery({
    queryKey: computed(() => (['listings', id])),
    queryFn: () => getListing(toValue(id)),
    enabled: computed(() => !!toValue(id)),
  })
}
