<script setup lang="ts">
import type { Listing } from '@/types/listings'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { can } from '@/lib/permissions.ts'
import { useCancelDonation, useConfirmListingDelivery, useGetActiveListings } from '@/services/listings.ts'
import { useCreateReview } from '@/services/reviews.ts'
import { useModal } from '@/utils/modal.ts'

const page = ref(1)
const perPage = ref(50)

const {
  data: donations,
  isInitialLoading,
  isError,
} = useGetActiveListings(page, perPage)

const router = useRouter()

function gotoListing(id: string) {
  router.push(`/oglasi/${id}`)
}

// Modals
const { showConfirmDeliveryModal, showFeedbackModal } = useModal()

// Mutations
const { mutateAsync: confirmArrival, isPending: isConfirming } = useConfirmListingDelivery()
const { mutateAsync: cancelDonationMutation, isPending: isCancelling } = useCancelDonation()
const { mutateAsync: createReview } = useCreateReview()

const toast = useToast()

async function handleConfirmArrivalClick(listing: Listing) {
  const confirmed = await showConfirmDeliveryModal()

  if (!confirmed)
    return

  try {
    await confirmArrival(listing.id)

    const feedbackResult = await showFeedbackModal(listing.owner.id, listing.owner.username)

    if (feedbackResult) {
      try {
        await createReview({
          for_listing: listing.id,
          rating: feedbackResult.rating,
          comment: feedbackResult.comment || undefined,
        })

        toast.add({
          title: 'Hvala na recenziji!',
          color: 'green',
        })
      }
      catch (error: any) {
        toast.add({
          title: 'Slanje recenzije neuspješno',
          description: error.message || 'Nepoznata greška',
          color: 'red',
        })
      }
    }
  }
  catch (error: any) {
    toast.add({
      title: 'Potvrda primopredaje neuspješna',
      description: error.message || 'Nepoznata pogreška',
      color: 'red',
    })
  }
}

async function handleCancelDonation(listing: Listing) {
  try {
    await cancelDonationMutation(listing.id)

    toast.add({
      title: 'Donacija otkazana',
      description: 'Uspješno ste otkazali donaciju. Oglas je sada dostupan drugim korisnicima.',
      color: 'green',
    })
  }
  catch (error: any) {
    toast.add({
      title: 'Otkazivanje neuspješno',
      description: error.message || 'Nepoznata pogreška',
      color: 'red',
    })
  }
}
</script>

<template>
  <template v-if="can('listings.view_listing')">
    <div class="flex items-center mr-6">
      <h2 class="font-medium text-2xl flex-1 text-neutral-900 mb-4">
        Aktivne donacije
      </h2>
    </div>
    <USkeleton v-if="isInitialLoading" class="h-48" />
    <UEmpty
      v-else-if="isError"
      icon="i-tabler-alert-square-rounded"
      title="Pogreška prilikom dohvaćanja"
      description="Došlo je do pogreške prilikom dohvaćanja aktivnih donacija. Molimo pokušajte ponovno kasnije."
    />
    <UEmpty
      v-else-if="donations?.results?.length === 0"
      icon="i-lucide-package"
      title="Nema aktivnih donacija"
      description="Ovdje će se pojaviti donacije koje su u fazi primopredaje."
      :ui="{ body: 'max-w-full' }"
    />
    <div v-else class="flex flex-col gap-2">
      <ListingCard v-for="donation in donations?.results" :key="donation.id" :listing="donation" @click="gotoListing(String(donation.id))">
        <template #actions>
          <div class="gap-2 flex">
            <UButton
              :ui="{ base: 'px-4 py-2 text-base', leadingIcon: 'size-6' }"
              color="success"
              icon="i-lucide:check"
              :loading="isConfirming"
              @click.stop="handleConfirmArrivalClick(donation)"
            >
              Potvrdi primopredaju
            </UButton>
            <UButton
              :ui="{ base: 'px-4 py-2 text-base', leadingIcon: 'size-6' }"
              color="error"
              variant="outline"
              icon="i-lucide-x"
              :loading="isCancelling"
              @click.stop="handleCancelDonation(donation)"
            >
              Odustani
            </UButton>
          </div>
        </template>
      </ListingCard>
    </div>
  </template>
</template>
