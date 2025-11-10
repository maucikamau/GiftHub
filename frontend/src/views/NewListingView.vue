<script setup lang="ts">
import type { ListingInput } from '@/types/listings.ts'
import { useQueryClient } from '@tanstack/vue-query'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import RegisteredUserLayout from '@/layouts/RegisteredUserLayout.vue'
import { listingInputSchema } from '@/schemas/listings.ts'
import { useCreateListing } from '@/services/listings.ts'
import { useGetCurrentUser } from '@/services/user.ts'

const router = useRouter()
const { data: user } = useGetCurrentUser()
const qc = useQueryClient()

const listingInput = ref<Partial<ListingInput>>({
  title: '',
  picture: '',
  content: '',
  category: '',
  location: user.value?.location || '',
  status: undefined,
  delivery: '',
})

const { mutate: publishListing } = useCreateListing()

function publish(listingInput: Partial<ListingInput>) {
  const listing = listingInputSchema.parse(listingInput)

  publishListing(listing, {
    onSuccess: () => {
      qc.invalidateQueries({
        queryKey: ['listings'],
      })
      router.push({ name: 'home' })
    },
  })
}
</script>

<template>
  <RegisteredUserLayout>
    <p class="text-xs mb-4">
      Oglasi / <span class="text-primary-400">Objavi novi oglas</span> / Potvrda
    </p>
    <ListingForm v-model="listingInput" @publish="publish" />
  </RegisteredUserLayout>
</template>
