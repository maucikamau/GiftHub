import type { Campaign, CampaignInput } from '@/types/campaigns.ts'
import type { PaginatedQuery } from '@/types/pagination.ts'
import { api } from '@/lib/apiClient.ts'
import { objectToFormData } from '@/utils/form.ts'

export async function getMyCampaigns() {
  return await api<Campaign[] | undefined>('campaigns/me/').json()
}

export async function createCampaign(campaign: CampaignInput) {
  const formData = objectToFormData(campaign)

  if (campaign.wish_list) {
    formData.set('wish_list', JSON.stringify(campaign.wish_list))
  }

  return await api<Campaign>('campaigns/create/', {
    method: 'POST',
    body: formData,
  }).json()
}

export async function updateCampaign(campaign: CampaignInput & { id: number }) {
  return await api<Campaign>(`campaigns/update/${campaign.id}/`, {
    method: 'PATCH',

    body: objectToFormData(campaign),
  }).json()
}

export async function getCampaign(id: number) {
  return await api<Campaign>(`campaigns/${id}/`).json()
}

export async function getCampaigns(page: number, perPage: number) {
  return await api<PaginatedQuery<Campaign> | undefined>('campaigns/', { searchParams: { page, perPage } }).json()
}
