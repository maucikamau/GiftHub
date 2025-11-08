import * as z from 'zod'

export const userSchema = z.object({
  first_name: z.string().min(1, 'Ime je obavezno'),
  last_name: z.string().min(1, 'Prezime je obavezno'),
  username: z.string().min(3, 'Korisničko ime mora imati najmanje 3 znaka'),
  email: z.email('Neispravna email adresa'),
  role: z.enum(['donor', 'recipient', 'recipient_individual', 'recipient_association']),
  location: z.string().min(1, 'Mjesto je obavezno'),
})

export const activeUserSchema = userSchema.extend({
  id: z.number(),
  registration_step: z.number().min(0).max(3),
})

export const associationSchema = z.object({
  association_name: z.string().min(1, 'Naziv udruge je obavezan'),
  association_email: z.email('Neispravna email adresa udruge'),
})

export const userBasicInfoSchema = userSchema.pick({
  first_name: true,
  last_name: true,
  username: true,
  location: true,
}).extend({
  termsAccepted: z.boolean().refine(val => val === true, {
    message: 'Morate prihvatiti uvjete korištenja',
  }),
})
