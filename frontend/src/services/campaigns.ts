import type { MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
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

export const useDonateToItem = (campaignId: MaybeRefOrGetter<number>) => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (itemName: string) => {
      const id = toValue(campaignId)

      const response = await fetch(`/api/campaigns/donate/${encodeURIComponent(itemName)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ campaign_id: id })
      })
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || 'Donacija nije uspjela')
      }
      return response.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns', toValue(campaignId)] })
    }
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

export function useUpdateCampaign() {
  return useMutation({
    mutationFn: updateCampaign,
  })
}