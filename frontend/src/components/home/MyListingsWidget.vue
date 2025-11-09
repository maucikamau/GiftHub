<script setup lang="ts">
import { useRouter } from 'vue-router'
import AppImage from '@/components/common/AppImage.vue'
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
      <UCard v-for="listing in listings" :key="listing.id" class="bg-transparent hover:bg-neutral-50 transition-colors" variant="soft" @click="openListing(listing.id)">
        <div class="flex gap-6">
          <div class="h-full w-60 flex-shrink-0">
            <AppImage
              :src="listing.picture ? listing.picture[0] : ''"
              :alt="listing.title"
              class="h-full"
              fallback-text="Nema slike"
            />
          </div>
          <div class="flex-1 flex flex-col">
            <div class="flex gap-4 items-end">
              <h3 class="font-bold text-2xl text-stone-900">
                {{ listing.title }}
              </h3>
              <h4 class="font-medium text-md text-stone-700">
                {{ listing.location }}
              </h4>
            </div>
            <p class="text-md font-medium text-stone-700 my-2 h-20">
              {{ listing.content }}
            </p>
            <div class="flex gap-4">
              <span class="font-medium text-stone-400">{{ listing.status }}</span>
              <span class="font-medium text-stone-400">{{ listing.category }}</span>
              <span class="font-medium text-stone-400">{{ listing.delivery }}</span>
            </div>
          </div>
          <div class="flex-shrink-0">
            <UButton
              :ui="{ base: 'px-4 py-2 text-base', leadingIcon: 'size-6' }"
              variant="outline"
              color="primary"
              icon="i-lucide:pencil"
              :to="`/oglasi/${listing.id}/uredi`"
              @click.stop="() => void 0"
            >
              Uredi oglas
            </UButton>
          </div>
        </div>
      </UCard>
    </div>
  </template>
</template>
