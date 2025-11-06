import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useListingsStore = defineStore('listings', () => {
  const listings = ref<Array<{ title: string, image: File, description: string, category: string, condition: string, delivery: string }>>([])

  function addListing(listing: { title: string, image: File, description: string, category: string, condition: string, delivery: string }) {
    listings.value.push(listing)
  }

  return { listings, addListing }
})
