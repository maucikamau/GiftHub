<script setup lang="ts">
import { computed, ref } from 'vue'
import NewListingConfirm from './NewListingConfirm.vue'

const lista_kategorija = ref(['Plišanci', 'Auti', 'Lutke'])
const lista_stanja = ref(['Rabljeno', 'Novo'])
const lista_dostava = ref(['Osobno preuzimanje', 'Dostava o trošku primatelja'])

const title = ref('')
const images = ref<File[]>([])
const description = ref('')
const category = ref('')
const condition = ref('')
const delivery = ref('')

const checklist = computed(() => [
  { label: 'Naslov', done: title.value.trim().length > 0 },
  { label: 'Slike', done: images.value.length > 0 },
  { label: 'Opis', done: description.value.trim().length > 0 },
  { label: 'Kategorija', done: !!category.value },
  { label: 'Stanje', done: !!condition.value },
  { label: 'Dostava', done: !!delivery.value },
])

const isComplete = computed(() => checklist.value.every(i => i.done))
const showConfirm = ref(false)
const newListingState = ref<any | null>(null)

function handleSubmit() {
  if (!isComplete.value)
    return

  const newListing = {
    title: title.value,
    images: images.value,
    description: description.value,
    category: category.value,
    condition: condition.value,
    delivery: delivery.value,
  }

  newListingState.value = newListing
  showConfirm.value = true
}

function onPublished() {
  title.value = ''
  images.value = []
  description.value = ''
  category.value = ''
  condition.value = ''
  delivery.value = ''
  showConfirm.value = false
}
</script>

<template>
  <form v-if="!showConfirm" @submit.prevent="handleSubmit">
    <div class="flex">
      <div class="w-3/5 mr-32">
        <div class="flex flex-col">
          <p class="text-xs mb-4">
            Oglasi / <span class="text-orange-400">Objavi novi oglas</span> / Potvrda
          </p>
          <h2 class="font-bold">Naslov</h2>
          <UInput v-model="title" class="w-full mb-6 font-bold" placeholder="Unesite naziv igračke" />
          <h2 class="font-bold">Slike (minimalno 1 slika)</h2>
          <UFileUpload v-model="images" accept="image/*,png/*,jpg/*" label="Dodajte ručno ili povucite slike koje želite objaviti uz oglas" multiple class="min-h-48 cursor-pointer mb-6" />
          <h2 class="font-bold">Opis</h2>
          <UTextarea v-model="description" :rows="8" class="mb-6" placeholder="Unesite opis igračke" />
          <div class="flex gap-8">
            <div>
              <h2 class="font-bold">Kategorija</h2>
              <USelect v-model="category" :items="lista_kategorija" class="w-56 h-12 mb-6" placeholder="Odaberite kategoriju" />
            </div>
            <div>
              <h2 class="font-bold">Stanje</h2>
              <URadioGroup v-model="condition" class="mb-6" orientation="horizontal" variant="card" default-value="" :items="lista_stanja" />
            </div>
          </div>
          <h2 class="font-bold">Dostava</h2>
          <URadioGroup v-model="delivery" orientation="horizontal" variant="card" default-value="" :items="lista_dostava" />
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
            <button
              type="submit"
              class="text-white font-bold py-2 px-4 rounded-full w-full max-w-sm transition-colors"
              :class="isComplete ? 'bg-green-500 hover:bg-green-700 cursor-pointer' : 'bg-green-200 cursor-not-allowed pointer-events-none'"
              :disabled="!isComplete"
            >
              Pregledaj i objavi oglas
            </button>
          </div>
        </aside>
      </div>
    </div>
  </form>
  <div v-else>
    <NewListingConfirm :listing="newListingState" @published="onPublished" @back="showConfirm = false" />
  </div>
</template>

<style scoped></style>
