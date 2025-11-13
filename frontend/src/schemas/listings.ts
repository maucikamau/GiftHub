import * as z from 'zod'
import { locationCitySchema, userSchema } from '@/schemas/user.ts'

export const ListingConditions = {
  new: 'Novo',
  used: 'Rabljeno',
  refurbished: 'Obnovljeno',
}

export const ListingDeliveryOptions = {
  pickup: 'Osobno preuzimanje',
  shipping: 'Dostava o trošku primatelja',
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
  owner: userSchema,
})

export const listingInputSchema = listingSchema
  .omit({ id: true, owner: true, picture: true, location: true })
  .extend({
    location: z.number().min(1, 'Lokacija je obvezna'),
    picture: z.custom<File>().refine(file => !!file, 'Slika je obvezna'),
  })
