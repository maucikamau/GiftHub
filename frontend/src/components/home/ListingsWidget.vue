<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useGetListings } from '@/services/listings.ts'

const page = ref(1)
const perPage = ref(50)

const {
  data: listings,
  isInitialLoading,
  isError,
} = useGetListings(page, perPage)

const router = useRouter()

function openListing(id: number) {
  router.push({ name: 'pregled-oglasa', params: { id } })
}
</script>

<template>
  <USkeleton v-if="isInitialLoading" class="h-48" />
  <UEmpty
    v-else-if="isError"
    icon="i-tabler-alert-square-rounded"
    title="Pogreška prilikom dohvaćanja"
    description="Došlo je do pogreške prilikom dohvaćanja vaših oglasa. Molimo pokušajte ponovno kasnije."
  />
  <UEmpty
    v-else-if="listings?.count === 0"
    icon="i-tabler-alert-square-rounded"
    title="Nema dostupnih oglasa."
    description="Trenutno nema dostupnih oglasa za prikaz."
    :ui="{ body: 'max-w-full' }"
  />
  <div v-else class="flex flex-col gap-2">
    <ListingCard v-for="listing in listings.results" :key="listing.id" :listing="listing" @click="openListing(listing.id)" />
  </div>
</template>
