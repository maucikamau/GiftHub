<script setup lang="ts">
import { useRouter } from 'vue-router'
import { can } from '@/lib/permissions.ts'
import { useGetMyListings } from '@/services/listings.ts'

const {
  data: listings,
  isInitialLoading,
  isError,
} = useGetMyListings()

const router = useRouter()

function openListing(id: number) {
  router.push({ name: 'pregled-oglasa', params: { id } })
}
</script>

<template>
  <template v-if="can('listings.add_listing')">
    <div class="flex items-center mx-6">
      <h2 class="font-medium text-2xl flex-1 text-neutral-900 mb-4">
        Moji oglasi
      </h2>
      <UButton
        :ui="{ base: 'px-4 py-2 text-base', leadingIcon: 'size-6' }"
        variant="solid"
        color="primary"
        icon="i-lucide:plus"
        to="/oglasi/novi"
        class="mb-4"
      >
        Novi oglas
      </UButton>
    </div>
    <USkeleton v-if="isInitialLoading" class="h-48" />
    <UEmpty
      v-else-if="isError"
      icon="i-tabler-alert-square-rounded"
      title="Pogreška prilikom dohvaćanja"
      description="Došlo je do pogreške prilikom dohvaćanja vaših oglasa. Molimo pokušajte ponovno kasnije."
    />
    <UEmpty
      v-else-if="listings?.length === 0"
      icon="i-tabler-alert-square-rounded"
      title="Još nemate oglasa"
      description="Izradite svoj prvi oglas."
      :ui="{ body: 'max-w-full' }"
    />
    <div v-else class="flex flex-col gap-2">
      <ListingCard v-for="listing in listings" :key="listing.id" :listing="listing" @click="openListing(listing.id)" />
    </div>
  </template>
</template>
