import type { MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { computed, toValue } from 'vue'
import {
  confirmListingDelivery,
  createListing,
  deleteListing,
  getActiveListings,
  getListing,
  getListings,
  getMyListings,
  updateListing,
} from '@/api/listings.ts'

export function useGetMyListings() {
  return useQuery({
    queryKey: ['listings', 'me'],
    queryFn: getMyListings,
    staleTime: 1000 * 30,
  })
}

export function useGetListings(
  page: MaybeRefOrGetter<number>,
  perPage: MaybeRefOrGetter<number>,
  filters?: MaybeRefOrGetter<{
    cityId?: number
    status?: string
    category?: string
  } | undefined>,
) {
  return useQuery({
    queryKey: computed(() => (['listings', toValue(page), toValue(perPage), toValue(filters)])),
    queryFn: () => getListings(toValue(page), toValue(perPage), toValue(filters)),
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
    onSuccess(_, variables, __, { client }) {
      return Promise.all([
        client.invalidateQueries({ queryKey: ['listings', variables.id] }),
        client.invalidateQueries({ queryKey: ['listings', 'me'] }),
      ])
    },
  })
}

export function useGetListing(id: MaybeRefOrGetter<number | undefined>) {
  return useQuery({
    queryKey: computed(() => (['listings', id])),
    queryFn: () => getListing(toValue(id)!),
    enabled: computed(() => !!toValue(id)),
    retry: false,
  })
}

export function useGetActiveListings(page: MaybeRefOrGetter<number>, perPage: MaybeRefOrGetter<number>) {
  return useQuery({
    queryKey: computed(() => (['active-donations', toValue(page), toValue(perPage)])),
    queryFn: () => getActiveListings(toValue(page), toValue(perPage)),
    enabled: computed(() => toValue(page) != null && toValue(perPage) != null),
  })
}

export function useConfirmListingDelivery() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: confirmListingDelivery,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['active-donations'] })
    },
  })
}

export function useDeleteListing() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: deleteListing,
    onSuccess: () => {
      // Invalidate all listing-related queries
      queryClient.invalidateQueries({ queryKey: ['listings'] })
      queryClient.invalidateQueries({ queryKey: ['active-donations'] })
    },
  })
}
