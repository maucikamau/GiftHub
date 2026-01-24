<script setup lang="ts">
import type { ChatConversation } from '@/types/chat.ts'
import { ref } from 'vue'
import { createStripeAccount, createStripeOnboardingLink, getStripeAccountStatus } from '@/api/payments.ts'
import { useGetCurrentUser } from '@/services/user.ts'

const props = defineProps<{
  forConversation: ChatConversation
}>()

const emit = defineEmits<{
  (e: 'close', success: boolean): void
}>()

const toast = useToast()
const { refetch: refetchUser } = useGetCurrentUser()
const isLoading = ref(false)
const isCheckingStatus = ref(false)

async function setupStripe() {
  isLoading.value = true

  try {
    await createStripeAccount().catch((error) => {
      if (!error?.message?.includes('already has')) {
        throw error
      }
    })

    const currentUrl = window.location.origin
    const callbackUrl = `${currentUrl}/stripe-callback?channel_id=${encodeURIComponent(props.forConversation.id)}`

    const { url } = await createStripeOnboardingLink({
      return_url: callbackUrl,
      refresh_url: callbackUrl,
    })

    // Redirect to Stripe onboarding
    window.location.href = url
  }
  catch (error: any) {
    console.error('Failed to setup Stripe:', error)

    const errorMessage = error?.message || 'Došlo je do greške prilikom povezivanja sa Stripe-om'

    toast.add({
      title: 'Povezivanje neuspješno',
      description: errorMessage,
      color: 'error',
    })

    isLoading.value = false
  }
}

async function checkStatusAndContinue() {
  isCheckingStatus.value = true

  try {
    const status = await getStripeAccountStatus()

    if (status.details_submitted && status.charges_enabled) {
      // Refetch user to update permissions
      await refetchUser()

      toast.add({
        title: 'Povezivanje uspješno',
        description: 'Sada možete slati zahtjeve za plaćanje.',
        color: 'success',
      })

      emit('close', true)
    }
    else {
      toast.add({
        title: 'Povezivanje nije dovršeno',
        description: 'Postavljanje može potrajati nekoliko minuta. Pokušajte ponovo kasnije.',
        color: 'warning',
      })
    }
  }
  catch (error: any) {
    console.error('Failed to check Stripe status:', error)

    toast.add({
      title: 'Greška pri provjeri statusa',
      description: error,
      color: 'error',
    })
  }
  finally {
    isCheckingStatus.value = false
  }
}
</script>

<template>
  <UModal title="Omogući plaćanja">
    <template #body>
      <div class="space-y-4">
        <div class="space-y-2">
          <p class="text-md font-semibold text-gray-800">
            PlayForward koristi Stripe za sigurno upravljanje plaćanjima.
          </p>
          <p class="text-sm text-gray-600">
            Stripe je siguran sustav za plaćanje koji omogućava primanje novca za troškove dostave.
            Proces povezivanja je brz i siguran.
          </p>
        </div>

        <div class="space-y-2">
          <p class="text-md text-gray-600">
            <strong>Što trebam?</strong>
          </p>
          <ul class="text-sm text-gray-600 pl-3 list-disc list-inside space-y-2">
            <li>Osobni podaci (ime, prezime, datum rođenja)</li>
            <li>Adresa prebivališta</li>
            <li>Broj telefona</li>
            <li>Podaci o bankovnom računu (IBAN)</li>
          </ul>
        </div>

        <UAlert
          icon="i-lucide:shield-check"
          color="success"
          variant="outline"
          title="Vaši podaci su sigurni"
          description="Mi ne pohranjujemo vaše osjetljive podatke. Pogledajte Stripe-ovu politiku privatnosti za više informacija."
        />
      </div>
    </template>
    <template #footer="{ close }">
      <UButton
        icon="i-lucide:link"
        label="Poveži Stripe"
        :loading="isLoading"
        :disabled="isLoading || isCheckingStatus"
        variant="solid"
        color="primary"
        @click="setupStripe"
      />
      <UButton
        label="Provjeri status"
        :loading="isCheckingStatus"
        :disabled="isLoading || isCheckingStatus"
        variant="outline"
        color="primary"
        @click="checkStatusAndContinue"
      />
      <UButton
        label="Odustani"
        color="neutral"
        variant="ghost"
        :disabled="isLoading || isCheckingStatus"
        @click="close"
      />
    </template>
  </UModal>
</template>

<style scoped>
</style>
