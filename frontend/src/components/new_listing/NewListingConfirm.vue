<script setup lang="ts">
import { computed } from 'vue'
import { useListingsStore } from '@/stores/listings'

const props = defineProps<{ listing: any | null }>()

const store = useListingsStore()

const title = computed(() => props.listing?.title ?? 'Title')
const description = computed(() => props.listing?.description ?? 'Description')
const category = computed(() => props.listing?.category ?? 'Category')
const condition = computed(() => props.listing?.condition ?? 'Condition')
const delivery = computed(() => props.listing?.delivery ?? 'Delivery')

function publish() {
  if (!props.listing) {
    return
  }

  store.addListing({
    title: props.listing.title,
    image: props.listing.images?.[0] ?? null,
    description: props.listing.description,
    category: props.listing.category,
    condition: props.listing.condition,
    delivery: props.listing.delivery,
  })
}
</script>

<template>
  <div class="flex flex-col">
    <p class="text-xs mb-4">
      Oglasi / Objavi novi oglas / <span class="text-orange-400">Potvrda</span>
    </p>
    <UCard>
      <div class="flex gap-6">
        <div class="w-40">
          <div
            class="w-40 aspect-[16/9] bg-gradient-to-t from-neutral-800 to-neutral-50 rounded-lg"
          />
        </div>
        <div class="flex-1 flex flex-col">
          <div class="flex gap-4 items-end">
            <h3 class="font-bold text-2xl text-stone-900">
              {{ title }}
            </h3>
            <h4 class="font-medium text-md text-stone-700">
              Mjesto
            </h4>
          </div>
          <p class="text-md font-medium text-stone-700 my-2 h-20">
            {{ description }}
          </p>
          <div class="flex gap-4">
            <span class="font-medium text-stone-400">{{ condition }}</span>
            <span class="font-medium text-stone-400">{{ category }}</span>
            <span class="font-medium text-stone-400">{{ delivery }}</span>
          </div>
        </div>
      </div>
    </UCard>
    <div class="flex justify-between text-center mt-6">
      <button class="text-white font-bold py-2 px-4 bg-orange-500 hover:bg-orange-700 cursor-pointer rounded-full max-w-sm transition-colors col-span-2 return-button" @click="$emit('back')">
        <p>← Natrag</p>
      </button>
      <button class="text-white font-bold py-2 px-4 bg-green-500 hover:bg-green-700 cursor-pointer rounded-full max-w-sm transition-colors col-span-2 return-button" @click="publish">
        <p>Objavi</p>
      </button>
    </div>
  </div>
</template>
