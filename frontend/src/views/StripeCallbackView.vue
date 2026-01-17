<script setup lang="ts">
import type { RouteLocationRaw } from 'vue-router'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getStripeAccountStatus } from '@/api/payments'
import CardLayout from '@/layouts/CardLayout.vue'
import { useGetCurrentUser } from '@/services/user.ts'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const { refetch: refetchUser } = useGetCurrentUser()

const isLoading = ref(true)
const statusMessage = ref('Provjeravanje statusa Stripe računa...')
const isSuccess = ref(false)

onMounted(async () => {
  try {
    // Check if Stripe account setup was completed
    const status = await getStripeAccountStatus()

    // Refetch user to update permissions
    await refetchUser()

    if (status.details_submitted && status.charges_enabled) {
      isSuccess.value = true
      statusMessage.value = 'Stripe račun uspješno povezan!'

      toast.add({
        title: 'Uspješno povezano',
        description: 'Vaš Stripe račun je uspješno povezan. Sada možete slati zahtjeve za plaćanje.',
        color: 'success',
      })

      const channelId = route.query.channel_id as string

      let redirectTo: RouteLocationRaw = { name: 'razgovori' }

      // Redirect to the chat conversation if we have a channel ID
      if (channelId) {
        redirectTo = { name: 'aktivan-razgovor', params: { id: channelId } }
      }
      setTimeout(() => router.push(redirectTo), 3000)
    }
    else {
      isSuccess.value = false
      statusMessage.value = 'Stripe konfiguracija nije potpuna'

      toast.add({
        title: 'Proces nije dovršen',
        description: 'Molimo dovršite proces povezivanja sa Stripe-om.',
        color: 'warning',
      })

      setTimeout(() => router.push({ name: 'razgovori' }), 3000)
    }
  }
  catch (error: any) {
    console.error('Failed to check Stripe status:', error)

    isSuccess.value = false
    statusMessage.value = 'Greška pri provjeri statusa'

    toast.add({
      title: 'Greška',
      description: error?.message || 'Nije moguće provjeriti status Stripe računa.',
      color: 'error',
    })

    setTimeout(() => {
      router.push({ name: 'razgovori' })
    }, 3000)
  }
  finally {
    isLoading.value = false
  }
})
</script>

<template>
  <CardLayout>
    <UCard class="max-w-md w-full">
      <template #header>
        <div class="flex items-center gap-3">
          <UIcon
            v-if="isLoading"
            name="i-lucide:loader-circle"
            class="w-6 h-6 animate-spin text-primary"
          />
          <UIcon
            v-else-if="isSuccess"
            name="i-lucide:check-circle"
            class="w-6 h-6 text-green-500"
          />
          <UIcon
            v-else
            name="i-lucide:alert-circle"
            class="w-6 h-6 text-orange-500"
          />
          <h2 class="text-xl font-semibold">
            Povratak sa Stripe-a
          </h2>
        </div>
      </template>

      <div class="space-y-4">
        <p class="text-gray-700">
          {{ statusMessage }}
        </p>

        <div v-if="isLoading" class="flex justify-center py-4">
          <UProgress animation="carousel" />
        </div>

        <UAlert
          v-else-if="isSuccess"
          icon="i-lucide:check"
          color="success"
          variant="soft"
          title="Uspješno!"
          description="Bit ćete preusmjereni na razgovor..."
        />

        <UAlert
          v-else
          icon="i-lucide:info"
          color="warning"
          variant="soft"
          title="Proces nije dovršen"
          description="Možete pokušati ponovno kasnije."
        />
      </div>

      <template #footer>
        <div class="flex justify-end">
          <UButton
            label="Idi na razgovore"
            color="primary"
            :disabled="isLoading"
            @click="router.push({ name: 'razgovori' })"
          />
        </div>
      </template>
    </UCard>
  </CardLayout>
</template>

<style scoped>
</style>
