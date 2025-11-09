import * as z from 'zod'
import { userSchema } from '@/schemas/user.ts'

const MAX_FILE_SIZE = 500000
const ACCEPTED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']

export const ListingConditions = {
  new: 'Novo',
  used: 'Rabljeno',
  refurbished: 'Obnovljeno',
}

export const listingSchema = z.object({
  id: z.number(),
  title: z.string().min(1, 'Naslov je obvezan').max(100, 'Naslov može imati najviše 100 znakova'),
  content: z.string().min(1, 'Opis je obvezan').max(1000, 'Opis može imati najviše 1000 znakova'),
  picture: z.array(z.url()).optional(),
  category: z.string().min(1, 'Category is required'),
  condition: z.enum(Object.keys(ListingConditions), 'Morate odabrati stanje igračke'),
  delivery: z.string().min(1, 'Delivery option is required'),
  location: z.string().min(1, 'Location is required'),
  owner: userSchema,
})

export const listingInputSchema = listingSchema
  .omit({ id: true, owner: true, picture: true })
  .extend({
    picture: z.array(z.custom<File>())
      .refine(files => files.length > 0, 'Barem jedna slika je obvezna.')
      .refine(files => files.every(f => f.size < MAX_FILE_SIZE), 'Slike moraju biti manje od 500KB.')
      .refine(
        files => files.every(f => ACCEPTED_IMAGE_TYPES.includes(f.type)),
        'Dozvoljeni formati slika su: JPEG, JPG, PNG, WEBP.',
      ),
  })
