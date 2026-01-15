import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDonationStore = defineStore('donations', () => {
  const donations = ref<Record<number, Record<string, number>>>({})

  const getDonationCount = (campaignId: number, itemName: string) => {
    return donations.value[campaignId]?.[itemName] || 0
  }

  const setDonationCount = (campaignId: number, itemName: string, count: number) => {
    if (!donations.value[campaignId]) {
      donations.value[campaignId] = {}
    }
    donations.value[campaignId][itemName] = count
  }

  return {
    donations,
    getDonationCount,
    setDonationCount,
  }
})
