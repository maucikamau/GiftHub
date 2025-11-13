import type { MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery } from '@tanstack/vue-query'
import { computed, toValue } from 'vue'
import {
  createListing,
  getListing,
  getListings,
  getMyListings,
  updateListing,
} from '@/api/listings.ts'

export function useGetMyListings() {
  return useQuery({
    queryKey: ['listings', 'me'],
    queryFn: getMyListings,
  })
}

export function useGetListings(page: MaybeRefOrGetter<number>, perPage: MaybeRefOrGetter<number>) {
  return useQuery({
    queryKey: computed(() => (['listings', toValue(page), toValue(perPage)])),
    queryFn: () => getListings(toValue(page), toValue(perPage)),
    enabled: computed(() => toValue(page) != null && toValue(perPage) != null),
  })
}

export function useCreateListing() {
  return useMutation({
    mutationFn: createListing,
  })
}

export function useUpdateListing() {
  return useMutation({
    mutationFn: updateListing,
  })
}

export function useGetListing(id: MaybeRefOrGetter<number>) {
  return useQuery({
    queryKey: computed(() => (['listings', id])),
    queryFn: () => getListing(toValue(id)),
    enabled: computed(() => !!toValue(id)),
    retry: false,
  })
}
