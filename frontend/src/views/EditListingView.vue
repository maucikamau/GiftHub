<script setup lang="ts">
import type { ListingInput } from '@/types/listings.ts'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import RegisteredUserLayout from '@/layouts/RegisteredUserLayout.vue'
import { useGetListing } from '@/services/listings.ts'

const route = useRoute('uredi-oglas')

const {
  data: listing,
  isLoading,
  error,
} = useGetListing(() => Number(route.params.id))

const listingInput = ref<Partial<ListingInput>>()

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

  listingInput.value = { ...newListing, picture }
}, { immediate: true })
</script>

<template>
  <RegisteredUserLayout>
    <USkeleton v-if="isLoading" class="w-full h-40" />
    <UEmpty
      v-if="error && error.message.includes('404')"
      title="Oglas nije pronađen"
      description="Oglas koji tražite ne postoji ili je uklonjen."
      icon="i-tabler:search-off"
    />
    <ListingForm v-if="listingInput" v-model="listingInput" />
  </RegisteredUserLayout>
</template>
