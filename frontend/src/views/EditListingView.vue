<script setup lang="ts">
import type { ListingInput } from '@/types/listings.ts'
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import RegisteredUserLayout from '@/layouts/RegisteredUserLayout.vue'
import { useGetListing, useUpdateListing } from '@/services/listings.ts'

const route = useRoute('uredi-oglas')
const router = useRouter()

const {
  data: listing,
  isLoading,
  error,
} = useGetListing(() => Number(route.params.id))

const { mutateAsync: updateListing } = useUpdateListing()

const listingInput = ref<Partial<ListingInput>>()

async function confirmUpdateListing(data: ListingInput) {
  // Handle the updated listing here

  const updatedListing = { ...data, id: Number(route.params.id) }

  await updateListing(updatedListing, {
    async onSuccess() {
      await router.push({ path: '/' })
    },
  })
}

watch(listing, async (newListing) => {
  // Convert picture URLs to File objects
  if (!newListing)
    return

  const picture = newListing.picture
    ? await fetch(newListing.picture)
        .then(res => res.blob())
        .then((blob) => {
          const filename = newListing.picture?.split('/').pop() || 'image.jpg'
          return new File([blob], filename, { type: blob.type })
        })
        .catch(() => '')
    : ''

  listingInput.value = { ...newListing, picture, location: newListing.location.id }
}, { immediate: true })
</script>

<template>
  <RegisteredUserLayout>
    <p class="text-sm mb-6">
      Oglasi / <span class="text-primary-600">Ažuriraj oglas</span>
    </p>
    <USkeleton v-if="isLoading" class="w-full h-40" />
    <UEmpty
      v-if="error && error.message.includes('404')"
      title="Oglas nije pronađen"
      description="Oglas koji tražite ne postoji ili je uklonjen."
      icon="i-tabler:search-off"
    />
    <ListingForm v-if="listingInput" v-model="listingInput" @publish="confirmUpdateListing" />
  </RegisteredUserLayout>
</template>
