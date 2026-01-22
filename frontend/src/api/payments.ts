import { api } from '@/lib/apiClient.ts'

export interface CreatePaymentIntentRequest {
  amount: number
  currency?: string
  chat_channel_id: string
}

export interface CreatePaymentIntentResponse {
  payment_id: number
  url: string
  stripe_payment_id: string
  amount: number
  currency: string
  listing_id: number
  donor_id: number
}

export interface StripeAccountStatus {
  id: number
  stripe_account_id: string
  charges_enabled: boolean
  payouts_enabled: boolean
  details_submitted: boolean
  created_at: string
  updated_at: string
}

export interface CreateOnboardingLinkRequest {
  return_url: string
  refresh_url: string
}

export interface CreateOnboardingLinkResponse {
  url: string
  expires_at: number
}

export async function createPaymentIntent(data: CreatePaymentIntentRequest) {
  return await api<CreatePaymentIntentResponse>('payments/payments/create-payment-intent/', {
    method: 'POST',
    json: {
      amount: data.amount,
      currency: data.currency || 'eur',
      chat_channel_id: data.chat_channel_id,
    },
  }).json().catch(async (err) => {
    const res = await err?.response.json()

    const exc = new Error(res?.error || 'Nepoznata pogreška. Pokušajte ponovo kasnije.')
    exc.status = res?.status || 500
    throw exc
  })
}

export async function createStripeAccount() {
  return await api('payments/accounts/link/', {
    method: 'POST',
  }).json().catch(async (err) => {
    const res = await err?.response.json()

    const exc = new Error(res?.error || 'Nepoznata pogreška prilikom kreiranja Stripe računa.')
    exc.status = res?.status || 500
    throw exc
  })
}

export async function createStripeOnboardingLink(data: CreateOnboardingLinkRequest) {
  return await api<CreateOnboardingLinkResponse>('payments/accounts/onboarding-link/', {
    method: 'POST',
    json: data,
  }).json().catch(async (err) => {
    const res = await err?.response.json()

    const exc = new Error(res?.error || 'Nepoznata pogreška prilikom kreiranja onboarding linka.')
    exc.status = res?.status || 500
    throw exc
  })
}

export async function getStripeAccountStatus() {
  return await api<StripeAccountStatus>('payments/accounts/account-status/', {
    method: 'GET',
  }).json().catch(async (err) => {
    const res = await err?.response.json()

    const exc = new Error(res?.error || 'Nepoznata pogreška prilikom dohvaćanja statusa.')
    exc.status = res?.status || 500
    throw exc
  })
}
