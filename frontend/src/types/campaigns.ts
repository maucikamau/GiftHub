import type { z } from 'zod'
import type { campaignInputSchema, campaignSchema } from '@/schemas/campaigns.ts'

export type Campaign = z.infer<typeof campaignSchema>

export type CampaignInput = z.infer<typeof campaignInputSchema>