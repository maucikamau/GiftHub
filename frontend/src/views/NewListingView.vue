<script setup lang="ts">
import type { ListingInput } from '@/types/listings.ts'
import { useQueryClient } from '@tanstack/vue-query'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
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
  location: user.value?.location?.id,
  status: undefined,
  delivery: '',
})

const { mutate: publishListing, isPending: isPublishing } = useCreateListing()
const toast = useToast()

function publish(listingInput: Partial<ListingInput>) {
  const listing = listingInputSchema.parse(listingInput)

  publishListing(listing, {
    onSuccess: () => {
      qc.invalidateQueries({
        queryKey: ['listings'],
      })
      router.push({ name: 'moji-oglasi' })
      toast.add({
        title: 'Oglas objavljen',
        description: 'Oglas je uspješno objavljen.',
        color: 'success',
      })
    },
  })
}
</script>

<template>
  <p class="text-sm mb-6">
    Oglasi / <span class="text-primary-600">Objavi novi oglas</span>
  </p>
  <ListingForm v-model="listingInput" :is-publishing="isPublishing" @publish="publish" />
</template>
