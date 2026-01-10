import type { MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery } from '@tanstack/vue-query'
import { computed, toValue } from 'vue'
import {
  createCampaign,
  getCampaign,
  getCampaigns,
  getMyCampaigns,
  updateCampaign,
} from '@/api/campaigns.ts'

export function useGetMyCampaigns() {
  return useQuery({
    queryKey: ['campaigns', 'me'],
    queryFn: getMyCampaigns,
  })
}

export function useGetCampaigns(page: MaybeRefOrGetter<number>, perPage: MaybeRefOrGetter<number>) {
  return useQuery({
    queryKey: computed(() => (['campaigns', toValue(page), toValue(perPage)])),
    queryFn: () => getCampaigns(toValue(page), toValue(perPage)),
    enabled: computed(() => toValue(page) != null && toValue(perPage) != null),
  })
}

export function useCreateCampaign() {
  return useMutation({
    mutationFn: createCampaign,
  })
}

export function useUpdateCampaign() {
  return useMutation({
    mutationFn: updateCampaign,
  })
}

export function useGetCampaign(id: MaybeRefOrGetter<number>) {
  return useQuery({
    queryKey: computed(() => (['campaigns', id])),
    queryFn: () => getCampaign(toValue(id)),
    enabled: computed(() => !!toValue(id)),
    retry: false,
  })
}
