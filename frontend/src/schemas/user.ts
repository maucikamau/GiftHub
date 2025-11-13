import * as z from 'zod'

export const locationCitySchema = z.object({
  id: z.number(),
  cityName: z.string().min(1, 'Grad je obavezan'),
})

export const userSchema = z.object({
  id: z.number().optional(),
  first_name: z.string().min(1, 'Ime je obavezno'),
  last_name: z.string().min(1, 'Prezime je obavezno'),
  username: z.string().min(3, 'Korisničko ime mora imati najmanje 3 znaka'),
  email: z.email('Neispravna email adresa'),
  role: z.enum(['donor', 'recipient', 'recipient_individual', 'recipient_association']),
  // location city is required, add message if not provided
  location: locationCitySchema,
})

export const activeUserSchema = userSchema.extend({
  id: z.number(),
  registration_step: z.number().min(0).max(3),
  permissions: z.array(z.string()),
})

export const associationSchema = z.object({
  association_name: z.string().min(1, 'Naziv udruge je obavezan'),
  association_email: z.email('Neispravna email adresa udruge'),
})

export const userBasicInfoSchema = userSchema.pick({
  first_name: true,
  last_name: true,
  username: true,
}).extend({
  location: z.number('Grad je obavezan'),
  termsAccepted: z.boolean().refine(val => val === true, {
    message: 'Morate prihvatiti uvjete korištenja',
  }),
})
