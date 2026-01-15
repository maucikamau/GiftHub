<script setup lang="ts">
import type { ChatConversationModel } from '@/lib/streamChat.ts'
import { ref } from 'vue'
import { createPaymentIntent } from '@/api/payments'

const { forConversation } = defineProps<{
  forConversation: ChatConversationModel
}>()

const emit = defineEmits<{
  (e: 'close', success: boolean): void
}>()

const toast = useToast()
const paymentAmount = ref<number>()
const isLoading = ref(false)

async function sendMessage() {
  if (!paymentAmount.value)
    return

  isLoading.value = true

  try {
    const response = await createPaymentIntent({
      amount: paymentAmount.value,
      currency: 'eur',
      chat_channel_id: forConversation.id,
    })

    toast.add({
      title: 'Uspješno kreiran zahtjev za plaćanje',
      description: `Zahtjev za plaćanje u iznosu od ${response.amount} ${response.currency.toUpperCase()} je uspješno kreiran.`,
      color: 'success',
    })

    emit('close', true)
  }
  catch (error: any) {
    console.error('Failed to create payment intent:', error)

    const errorMessage = error?.data?.error || error?.message || 'Došlo je do greške prilikom kreiranja zahtjeva za plaćanje'

    toast.add({
      title: 'Greška',
      description: errorMessage,
      color: 'error',
    })
  }
  finally {
    isLoading.value = false
  }
}
</script>

<template>
  <UModal title="Zatraži plaćanje dostave">
    <template #body>
      <UFormField label="Iznos dostave (€)">
        <template #description>
          <p>Primatelj će dobiti račun za plaćanje dostave. Nakon obavljenog plaćanja, možete nastaviti sa dostavom u suradnji sa kurirskom službom.</p>
        </template>
        <UInput
          v-model="paymentAmount"
          type="number"
          label="Iznos dostave (€)"
          placeholder="npr. 4,25 €"
          size="lg"
          class="w-full"
        />
      </UFormField>
    </template>
    <template #footer="{ close }">
      <UButton
        icon="i-lucide:check"
        label="Pošalji"
        :disabled="!paymentAmount || isLoading"
        :loading="isLoading"
        :variant="paymentAmount ? 'solid' : 'soft'"
        color="primary"
        @click="sendMessage"
      />
      <UButton label="Otkaži" color="neutral" variant="ghost" :disabled="isLoading" @click="close" />
    </template>
  </UModal>
</template>

<style scoped>

</style>
