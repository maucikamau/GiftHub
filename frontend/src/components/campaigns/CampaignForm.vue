<script setup lang="ts">
import type { Campaign, CampaignInput } from '@/types/campaigns'
import { computed, ref } from 'vue'
import { treeifyError } from 'zod'
import { campaignInputSchema } from '@/schemas/campaigns.ts'
import { useGetCities } from '@/services/user.ts'
import NewCampaignConfirm from './NewCampaignConfirm.vue'

defineEmits<{
  (e: 'publish', campaign: CampaignInput): void
}>()
const campaignInput = defineModel<Partial<CampaignInput>>({ required: true })

const showConfirm = ref(false)
const { data: cities } = useGetCities()

const checklist = computed(() => {
  const campaign = campaignInputSchema.safeParse(campaignInput.value)

  const errors = campaign.success ? {} : treeifyError(campaign.error).properties ?? {}

  return [
    { label: 'Naslov', done: !('title' in errors) },
    { label: 'Slike', done: !('picture' in errors) },
    { label: 'Opis', done: !('content' in errors) },
    { label: 'Lokacija', done: !('location' in errors) },
  ]
})
const isComplete = computed(() => checklist.value.every(i => i.done))

function toCampaign(input: Partial<CampaignInput>): Campaign {
  return {
    ...input,
    location: cities.value?.find(c => c.id === input.location) || { id: 0, cityName: 'Nepoznato' },
  }
}

function handleSubmit() {
  showConfirm.value = true
}
</script>

<template>
  <div v-if="!showConfirm">
    <UForm :schema="campaignInputSchema" :state="campaignInput" class="flex" @submit.prevent="handleSubmit">
      <div class="w-3/5 mr-32">
        <div class="flex flex-col">
          <UFormField label="Naslov">
            <UInput v-model="campaignInput.title" class="w-full mb-6 font-bold" size="xl" placeholder="Unesite naziv kampanje" />
          </UFormField>
          <UFormField label="Slike" hint="1 slika">
            <UFileUpload v-model="campaignInput.picture" accept="image/*,png/*,jpg/*" label="Dodajte ručno ili povucite slike koje želite objaviti" class="min-h-48 cursor-pointer mb-6" />
          </UFormField>
          <h2 class="font-bold">
            Opis
          </h2>
          <UTextarea v-model="campaignInput.content" :rows="8" class="mb-6" placeholder="Unesite opis kampanje" />
          <div class="flex flex-1 gap-8">
            <div class="flex-1 flex-shrink-0">
              <h2 class="font-bold">
                Lokacija
              </h2>
              <USelectMenu
                v-model="campaignInput.location"
                label-key="cityName"
                value-key="id"
                :items="cities"
                class="w-full h-10"
                size="xl"
                placeholder="Odaberite mjesto"
              />
            </div>
          </div>
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
  <NewCampaignConfirm v-else :campaign="toCampaign(campaignInput)" @confirm="$emit('publish', campaignInput as CampaignInput)" @back="showConfirm = false" />
</template>
