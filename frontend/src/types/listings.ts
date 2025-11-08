import type { z } from 'zod'
import type { listingInputSchema, listingSchema } from '@/schemas/listings.ts'

export type Listing = z.infer<typeof listingSchema>

export type ListingInput = z.infer<typeof listingInputSchema>
