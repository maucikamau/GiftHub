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

export const ListingStatus = {
  available: 'Dostupno',
  accepted_donation: 'Prihvaćena donacija',
  payment_requested: 'Zatražena uplata za dostavu',
  waiting_for_pickup: 'Čeka potvrdu primopredaje',
  completed: 'Završeno',
}

export const listingSchema = z.object({
  id: z.number(),
  title: z.string().min(1, 'Naslov je obvezan').max(100, 'Naslov može imati najviše 100 znakova'),
  content: z.string().min(1, 'Opis je obvezan').max(1000, 'Opis može imati najviše 1000 znakova'),
  picture: z.url().optional(),
  category: z.string().min(1, 'Category is required'),
  condition: z.enum(Object.keys(ListingConditions), 'Morate odabrati stanje igračke'),
  delivery: z.enum(Object.keys(ListingDeliveryOptions), 'Morate odabrati način preuzimanja'),
  status: z.enum(Object.keys(ListingStatus)),
  conversation_id: z.string().optional(),
  location: locationCitySchema,
  owner: userOwnerSchema,
})

export const listingInputSchema = listingSchema
  .omit({ id: true, owner: true, picture: true, location: true, status: true, conversation_id: true })
  .extend({
    location: z.number().min(1, 'Lokacija je obvezna'),
    picture: z.custom<File>().refine(file => !!file, 'Slika je obvezna'),
  })

// TODO: convert to Django model
export const toyCategories
  = [
    'Plišanci',
    'Lutke',
    'Autići i vozila',
    'Figurice',
    'Kocke i konstrukcijske igračke',
    'Puzzle i slagalice',
    'Društvene igre',
    'Karte za igranje',
    'Glazbene igračke',
    'Instrumenti',
    'Kreativne igračke',
    'Umjetničke igračke',
    'Modeliranje (plastelin, pijesak)',
    'Edukativne igračke',
    'Elektroničke igračke',
    'Drvene igračke',
    'Magnetne igračke',
    'Igračke za bebe',
    'Senzorne i motoričke igračke',
    'Igračke za van',
    'Sportske igračke',
    'Igre logike i memorije',
    'Kućice i pribor za lutke',
    'Maštovite i kostimske igračke',
    'Tematske igračke',
    'Ekološki prihvatljive igračke',
    'Ostalo',
  ]
