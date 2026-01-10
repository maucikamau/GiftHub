import * as z from 'zod'
import { locationCitySchema, userOwnerSchema } from '@/schemas/user.ts'

export const campaignSchema = z.object({
  id: z.number(),
  title: z.string().min(1, 'Naslov je obvezan').max(100, 'Naslov može imati najviše 100 znakova'),
  content: z.string().min(1, 'Opis je obvezan').max(1000, 'Opis može imati najviše 1000 znakova'),
  picture: z.url().optional(),
  location: locationCitySchema,
  owner: userOwnerSchema,
})

export const campaignInputSchema = campaignSchema
  .omit({ id: true, owner: true, picture: true, location: true })
  .extend({
    location: z.number().min(1, 'Lokacija je obvezna'),
    picture: z.custom<File>().refine(file => !!file, 'Slika je obvezna'),
  })
