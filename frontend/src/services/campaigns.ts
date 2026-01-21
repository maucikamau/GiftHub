import type { MaybeRefOrGetter } from 'vue'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { computed, toValue } from 'vue'
import {
  createCampaign,
  deleteCampaign,
  donateToCampaign,
  getCampaign,
  getCampaigns,
  getMyCampaigns,
  updateCampaign,
} from '@/api/campaigns.ts'

export function useGetMyCampaigns() {
  return useQuery({
    queryKey: ['campaigns', 'me'],
    queryFn: getMyCampaigns,
    staleTime: 1000 * 30,
  })
}

export function useGetCampaigns(page: MaybeRefOrGetter<number>, perPage: MaybeRefOrGetter<number>) {
  return useQuery({
    queryKey: computed(() => (['campaigns', toValue(page), toValue(perPage)])),
    queryFn: () => getCampaigns(toValue(page), toValue(perPage)),
    enabled: computed(() => toValue(page) != null && toValue(perPage) != null),
    staleTime: 1000 * 60,
  })
}

export function useCreateCampaign() {
  return useMutation({
    mutationFn: createCampaign,
  })
}

export function useDonateToCampaign() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ itemName, campaignId }: { itemName: string, campaignId: number }) =>
      donateToCampaign(itemName, campaignId),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['campaigns', variables.campaignId] })
    },
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
    onSuccess(_, variables, __, { client }) {
      return Promise.all([
        client.invalidateQueries({ queryKey: ['campaigns', variables.id] }),
        client.invalidateQueries({ queryKey: ['campaigns', 'me'] }),
      ])
    },
  })
}

export function useDeleteCampaign() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: deleteCampaign,
    onSuccess: () => {
      // Invalidate all campaign-related queries
      queryClient.invalidateQueries({ queryKey: ['campaigns'] })
    },
  })
}
