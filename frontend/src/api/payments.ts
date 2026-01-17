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
