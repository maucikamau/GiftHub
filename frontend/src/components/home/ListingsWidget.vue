<script setup lang="ts">
import { watchDebounced } from '@vueuse/core'
import { OverlayScrollbarsComponent } from 'overlayscrollbars-vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ListingDeliveryOptions, toyCategories } from '@/schemas/listings.ts'
import { useGetListings } from '@/services/listings.ts'

const page = ref(1)
const perPage = ref(50)

// Filter states
const cityFilter = ref('')
const deliveryFilter = ref<string>('')
const categoryFilter = ref<string>('')

// Computed filters object
const filters = ref()

watchDebounced(
  [cityFilter, deliveryFilter, categoryFilter],
  () => {
    filters.value = {
      ...(cityFilter.value ? { city: cityFilter.value } : {}),
      ...(deliveryFilter.value ? { delivery_option: deliveryFilter.value } : {}),
      ...(categoryFilter.value ? { category: categoryFilter.value } : {}),
    }
  },
  { debounce: 300, immediate: true },
)

const {
  data: listings,
  isInitialLoading,
  isError,
} = useGetListings(page, perPage, filters)

const router = useRouter()

function openListing(id: number) {
  router.push({ name: 'pregled-oglasa', params: { id } })
}

// Status options for dropdown
const statusOptions = [
  ...Object.values(ListingDeliveryOptions).map(opt => ({ label: opt.label, value: opt.value })),
]

// Category options for dropdown
const categoryOptions = [
  ...toyCategories.map(cat => ({ label: cat, value: cat })),
]

// Reset page to 1 when filters change
function resetPage() {
  page.value = 1
}
</script>

<template>
  <div class="mb-4 flex flex-wrap gap-3">
    <UInput
      v-model="cityFilter"
      placeholder="Pretraži po gradu..."
      icon="i-lucide:search"
      class="min-w-48"
      @update:model-value="resetPage"
    />
    <USelectMenu
      v-model="deliveryFilter"
      :items="statusOptions"
      label-key="label"
      value-key="value"
      placeholder="Status"
      class="min-w-48"
      clear
      @update:model-value="resetPage"
    />
    <USelectMenu
      v-model="categoryFilter"
      :items="categoryOptions"
      label-key="label"
      value-key="value"
      placeholder="Kategorija"
      clear
      class="min-w-48"
      @update:model-value="resetPage"
    />
  </div>
  <OverlayScrollbarsComponent class="h-full overflow-auto">
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
      <ListingCard
        v-for="listing in listings?.results" :key="listing.id" :listing="listing"
        @click="openListing(listing.id)"
      />
    </div>
  </OverlayScrollbarsComponent>
  <div class="flex gap-3 justify-end py-4">
    <UPagination
      v-if="listings && listings.count > perPage"
      :page="page"
      :items-per-page="perPage"
      :total="listings.count"
      @update:page="(newPage) => (page = newPage)"
    />
  </div>
</template>
