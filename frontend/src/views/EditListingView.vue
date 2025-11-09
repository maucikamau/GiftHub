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

const listingInput = ref<Partial<ListingInput>>({})

watch(listing, async (newListing) => {
  // Convert picture URLs to File objects
  const pictures = await Promise.all<File>(newListing?.picture?.map(async (url) => {
    return fetch(url)
      .then(res => res.blob())
      .then((blob) => {
        const filename = url.split('/').pop() || 'image.jpg'
        return new File([blob], filename, { type: blob.type })
      })
  }) || [])
  if (newListing) {
    listingInput.value = { ...newListing, picture: pictures }
  }
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
    <ListingForm v-model="listingInput" />
  </RegisteredUserLayout>
</template>
