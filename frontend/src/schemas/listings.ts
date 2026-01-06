import * as z from 'zod'
import { locationCitySchema, userOwnerSchema } from '@/schemas/user.ts'

export const ListingConditions = {
  new: 'Novo',
  used: 'Rabljeno',
  refurbished: 'Obnovljeno',
}

interface ListingDeliveryOption {
  label: string
  description: string
  value: string
}

export const ListingDeliveryOptions: Record<'pickup' | 'shipping', ListingDeliveryOption> = {
  pickup: {
    label: 'Osobno preuzimanje',
    description: 'Preuzmite igračku osobno na dogovorenoj lokaciji s oglašivačem. Nema dodatnih troškova.',
    value: 'pickup',
  },
  shipping: {
    label: 'Dostava o trošku primatelja',
    description: 'Zatražite dostavu na Vašu adresu. Troškove će obračunati oglašivač na temelju procjene dostavljača. Vi snosite troškove dostave.',
    value: 'shipping',
  },
}

export const listingSchema = z.object({
  id: z.number(),
  title: z.string().min(1, 'Naslov je obvezan').max(100, 'Naslov može imati najviše 100 znakova'),
  content: z.string().min(1, 'Opis je obvezan').max(1000, 'Opis može imati najviše 1000 znakova'),
  picture: z.url().optional(),
  category: z.string().min(1, 'Category is required'),
  condition: z.enum(Object.keys(ListingConditions), 'Morate odabrati stanje igračke'),
  delivery: z.enum(Object.keys(ListingDeliveryOptions), 'Morate odabrati način preuzimanja'),
  location: locationCitySchema,
  owner: userOwnerSchema,
})

export const listingInputSchema = listingSchema
  .omit({ id: true, owner: true, picture: true, location: true })
  .extend({
    location: z.number().min(1, 'Lokacija je obvezna'),
    picture: z.custom<File>().refine(file => !!file, 'Slika je obvezna'),
  })
