<script setup lang="ts">
import { useRoute } from 'vue-router'
import RegisteredUserLayout from '@/layouts/RegisteredUserLayout.vue'
import { useGetListing } from '@/services/listings.ts'
import { useGetCurrentUser } from '@/services/user.ts'
import { useNotImplementedModal } from '@/utils/modal.ts'

const route = useRoute('pregled-oglasa')
const { data: user } = useGetCurrentUser()

const { showNotImplementedModal } = useNotImplementedModal()

const {
  data: listing,
  isLoading,
  error,
} = useGetListing(() => Number(route.params.id))
</script>

<template>
  <RegisteredUserLayout wide>
    <USkeleton v-if="isLoading" class="w-full h-40" />
    <UEmpty
      v-if="error && error.message.includes('404')"
      title="Oglas nije pronađen"
      description="Oglas koji tražite ne postoji ili je uklonjen."
      icon="i-tabler:search-off"
    />
    <div v-else-if="listing" class="flex flex-col 2xl:flex-row justify-between gap-20">
      <ListingPreview :listing="listing" />
      <div class="2xl:w-sm flex flex-col gap-4">
        <UCard variant="soft" color="primary" class="w-full 2xl:flex-none">
          <template #header>
            <h2 class="font-semibold text-md">
              Objavio
            </h2>
            <UUser
              :name="`@${listing.owner.username}`"
              size="xl"
              class="w-full my-4"
              :ui="{ name: 'text-2xl font-semibold' }"
            />
            <div class="flex">
              <div class="text-2xl font-medium gap-2 flex items-end">
                <span class="text-6xl">4.5</span>/5
              </div>
              <div class="flex flex-col ml-4">
                <div class="flex items-center gap-1 ml-2">
                  <UIcon name="solar:star-bold-duotone" class="size-7 text-yellow-400" />
                  <UIcon name="solar:star-bold-duotone" class="size-7 text-yellow-400" />
                  <UIcon name="solar:star-bold-duotone" class="size-7 text-yellow-400" />
                  <UIcon name="solar:star-bold-duotone" class="size-7 text-yellow-400" />
                  <UIcon name="solar:star-bold-duotone" class="size-7 text-neutral-600" />
                </div>
                <UButton variant="ghost" trailing-icon="i-tabler:arrow-right" size="sm" class="mt-1">
                  Pogledaj recenzije
                </UButton>
              </div>
            </div>
          </template>
        </UCard>

        <template
          v-if="listing.owner.id !== user?.id"
        >
          <UButton size="xl" class="h-12" color="primary" variant="solid" block>
            <UIcon name="i-solar:chat-round-line-outline" class="size-7 mr-2" />
            Započni razgovor
          </UButton>
          <UButton size="xl" class="h-12" color="secondary" variant="solid" block>
            <UIcon name="i-iconoir:donate" class="size-7 mr-2" />
            Pošalji zahtjev za donaciju
          </UButton>
        </template>
        <template v-else>
          <UButton leading-icon="i-lucide:pencil" size="xl" class="h-12" color="primary" variant="solid" block :to="`/oglasi/${listing.id}/uredi`">
            Uredi oglas
          </UButton>
          <UButton leading-icon="i-lucide:trash" size="xl" class="h-12" color="error" variant="solid" block @click="showNotImplementedModal()">
            Obriši oglas
          </UButton>
        </template>
      </div>
    </div>
  </RegisteredUserLayout>
</template>
