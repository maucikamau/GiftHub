<script setup lang="ts">
import type { ListingInput } from '@/types/listings'
import { useQueryClient } from '@tanstack/vue-query'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { treeifyError } from 'zod'
import { listingInputSchema } from '@/schemas/listings.ts'
import { useCreateListing } from '@/services/listings.ts'
import { useUserStore } from '@/stores/user.ts'
import NewListingConfirm from './NewListingConfirm.vue'

const categoryOptions = ref(['Plišanci', 'Auti', 'Lutke'])
const conditionOptions = ref([{ label: 'Rabljeno', value: 'used' }, { label: 'Novo', value: 'new' }])
const deliveryOptions = ref(['Osobno preuzimanje', 'Dostava o trošku primatelja'])

const showConfirm = ref(false)
const router = useRouter()
const qc = useQueryClient()
const userStore = useUserStore()

const listingInput = ref<Partial<ListingInput>>({
  title: '',
  picture: [],
  content: '',
  category: '',
  location: userStore.user?.location || '',
  status: undefined,
  delivery: '',
})

const checklist = computed(() => {
  const listing = listingInputSchema.safeParse(listingInput.value)

  const errors = listing.success ? {} : treeifyError(listing.error).properties ?? {}

  return [
    { label: 'Naslov', done: !('title' in errors) },
    { label: 'Slike', done: !('picture' in errors) },
    { label: 'Opis', done: !('content' in errors) },
    { label: 'Kategorija', done: !('category' in errors) },
    { label: 'Stanje', done: !('status' in errors) },
    { label: 'Lokacija', done: !('location' in errors) },
    { label: 'Dostava', done: !('delivery' in errors) },
  ]
})
const isComplete = computed(() => checklist.value.every(i => i.done))

function handleSubmit() {
  showConfirm.value = true
}

const { mutate: publishListing } = useCreateListing()

function publish() {
  const listing = listingInputSchema.parse(listingInput.value)

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
  <UForm v-if="!showConfirm" :schema="listingInputSchema" :state="listingInput" @submit.prevent="handleSubmit">
    <div class="flex">
      <div class="w-3/5 mr-32">
        <div class="flex flex-col">
          <p class="text-xs mb-4">
            Oglasi / <span class="text-primary-400">Objavi novi oglas</span> / Potvrda
          </p>
          <UFormField label="Naslov">
            <UInput v-model="listingInput.title" class="w-full mb-6 font-bold" placeholder="Unesite naziv igračke" />
          </UFormField>
          <UFormField label="Slike" hint="min. 1 slika">
            <UFileUpload v-model="listingInput.picture" accept="image/*,png/*,jpg/*" label="Dodajte ručno ili povucite slike koje želite objaviti uz oglas" multiple class="min-h-48 cursor-pointer mb-6" />
          </UFormField>
          <h2 class="font-bold">
            Opis
          </h2>
          <UTextarea v-model="listingInput.content" :rows="8" class="mb-6" placeholder="Unesite opis igračke" />
          <div class="flex flex-1 gap-8">
            <div class="flex-1 flex-shrink-0">
              <h2 class="font-bold">
                Kategorija
              </h2>
              <USelect v-model="listingInput.category" class="w-full" :items="categoryOptions" size="xl" placeholder="Odaberite kategoriju" />
            </div>
            <div class="flex-1 flex-shrink-0">
              <h2 class="font-bold">
                Lokacija
              </h2>
              <UInput v-model="listingInput.location" class="w-full" size="xl" placeholder="Odaberite kategoriju" />
            </div>
          </div>
          <div class="mt-6">
            <h2 class="font-bold">
              Stanje
            </h2>
            <URadioGroup v-model="listingInput.status" class="mb-6" orientation="horizontal" variant="card" value-key="value" :items="conditionOptions" />
          </div>
          <h2 class="font-bold">
            Dostava
          </h2>
          <URadioGroup v-model="listingInput.delivery" orientation="horizontal" variant="card" default-value="" :items="deliveryOptions" />
        </div>
      </div>
      <div class="w-2/5">
        <aside class="sticky top-6">
          <h3 class="text-lg mb-3 font-bold">
            Provjera
          </h3>
          <ul class="space-y-2">
            <li v-for="item in checklist" :key="item.label" class="flex items-center justify-between p-3 border border-gray-200 rounded">
              <span>{{ item.label }}</span>
              <span v-if="item.done" class="text-green-600 font-bold">✓</span>
              <span v-else class="text-gray-400">—</span>
            </li>
          </ul>
          <div class="mt-8 flex justify-center text-center">
            <UButton
              type="submit"
              color="success"
              block
              size="xl"
              :disabled="!isComplete"
            >
              Pregledaj i objavi oglas
            </UButton>
          </div>
        </aside>
      </div>
    </div>
  </UForm>
  <div v-else>
    <NewListingConfirm :listing="listingInput" @confirm="publish" @back="showConfirm = false" />
  </div>
</template>

<style scoped></style>
