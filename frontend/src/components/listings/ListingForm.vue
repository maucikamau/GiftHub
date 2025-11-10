<script setup lang="ts">
import type { ListingInput } from '@/types/listings'
import { computed, ref } from 'vue'
import { treeifyError } from 'zod'
import { ListingConditions, ListingDeliveryOptions, listingInputSchema } from '@/schemas/listings.ts'
import NewListingConfirm from './NewListingConfirm.vue'

defineEmits<{
  (e: 'publish', listing: ListingInput): void
}>()
const listingInput = defineModel<Partial<ListingInput>>({ required: true })
const categoryOptions = ref(['Plišanci', 'Auti', 'Lutke'])
const conditionOptions = Object.entries(ListingConditions).map(([key, label]) => ({ label, value: key }))
const deliveryOptions = Object.entries(ListingDeliveryOptions).map(([key, label]) => ({ label, value: key }))

const showConfirm = ref(false)

const checklist = computed(() => {
  const listing = listingInputSchema.safeParse(listingInput.value)

  const errors = listing.success ? {} : treeifyError(listing.error).properties ?? {}

  return [
    { label: 'Naslov', done: !('title' in errors) },
    { label: 'Slike', done: !('picture' in errors) },
    { label: 'Opis', done: !('content' in errors) },
    { label: 'Kategorija', done: !('category' in errors) },
    { label: 'Stanje', done: !('condition' in errors) },
    { label: 'Lokacija', done: !('location' in errors) },
    { label: 'Dostava', done: !('delivery' in errors) },
  ]
})
const isComplete = computed(() => checklist.value.every(i => i.done))

function handleSubmit() {
  showConfirm.value = true
}
</script>

<template>
  <div v-if="!showConfirm">
    <UForm :schema="listingInputSchema" :state="listingInput" class="flex" @submit.prevent="handleSubmit">
      <div class="w-3/5 mr-32">
        <div class="flex flex-col">
          <UFormField label="Naslov">
            <UInput v-model="listingInput.title" class="w-full mb-6 font-bold" size="xl" placeholder="Unesite naziv igračke" />
          </UFormField>
          <UFormField label="Slike" hint="1 slika">
            <UFileUpload v-model="listingInput.picture" accept="image/*,png/*,jpg/*" label="Dodajte ručno ili povucite slike koje želite objaviti uz oglas" class="min-h-48 cursor-pointer mb-6" />
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
            <URadioGroup v-model="listingInput.condition" class="mb-6" orientation="horizontal" variant="card" value-key="value" :items="conditionOptions" />
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
              to=""
              size="xl"
              :disabled="!isComplete"
            >
              Pregledaj i objavi oglas
            </UButton>
          </div>
        </aside>
      </div>
    </UForm>
  </div>
  <NewListingConfirm v-else :listing="listingInput as ListingInput" @confirm="$emit('publish', listingInput as ListingInput)" @back="showConfirm = false" />
</template>
