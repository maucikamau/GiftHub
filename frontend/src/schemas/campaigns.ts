import * as z from 'zod'
import { locationCitySchema, userOwnerSchema } from '@/schemas/user.ts'

export const campaignSchema = z.object({
  id: z.number(),
  title: z.string().min(1, 'Naslov je obvezan').max(100, 'Naslov može imati najviše 100 znakova'),
  description: z.string().min(1, 'Opis je obvezan').max(1000, 'Opis može imati najviše 1000 znakova'),
  picture: z.url().optional(),
  location: locationCitySchema,
  owner: userOwnerSchema,
  end_date: z.string().refine(
    (value) => !isNaN(Date.parse(value)),
    'Neispravan datum završetka'
  ),
  wish_list: z.array(z.object({
    name: z.string(),
    count: z.number(),
    donated: z.number(),
  })),
})

export const campaignInputSchema = campaignSchema
  .omit({ id: true, owner: true, picture: true, location: true, wish_list: true })
  .extend({
    location: z.number().min(1, 'Lokacija je obvezna'),
    picture: z.custom<File>().refine(file => !!file, 'Slika je obvezna'),
    end_date: z.string()
      .refine(v => !isNaN(Date.parse(v)), 'Neispravan datum')
      .refine(v => new Date(v) > new Date(), 'Datum mora biti u budućnosti'),
    wish_list: z.array(z.object({
      name: z.string().min(1, 'Naziv je obvezan'),
      count: z.number().min(1, 'Količina mora biti najmanje 1').max(100, 'Količina može biti najviše 100'),
      donated: z.number().optional().default(0),
    })).min(1, 'Morate dodati bar jednu igračku'),
  })
