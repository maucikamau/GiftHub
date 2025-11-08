<script setup lang="ts">
import { useRoute } from 'vue-router'
import RegisteredUserLayout from '@/layouts/RegisteredUserLayout.vue'
import { useGetListing } from '@/services/listings.ts'

const route = useRoute('pregled-oglasa')

const {
  data: listing,
  isInitialLoading,
  isError,
} = useGetListing(() => Number(route.params.id))
</script>

<template>
  <RegisteredUserLayout wide>
    <div v-if="listing" class="flex flex-col 2xl:flex-row justify-between gap-20">
      <div class="flex-1 2xl:max-w-4xl">
        <h2 class="text-4xl font-bold my-4 text-neutral-900">
          {{ listing.title }}
        </h2>
        <div class="flex flex-col lg:flex-row gap-4 justify-between mb-8">
          <h4 class="text-lg font-medium text-neutral-400">
            {{ listing.location }}
          </h4>
          <div class="flex gap-4">
            <h4 class="text-md text-neutral-400">
              {{ listing.status }}
            </h4>
            <h4 class="text-md text-neutral-400">
              {{ listing.category }}
            </h4>
            <h4 class="text-md text-neutral-400">
              {{ listing.delivery }}
            </h4>
          </div>
        </div>
        <AppImage :src="listing?.picture" class="aspect-video w-full shadow-sm" />
        <div class="my-4">
          {{ listing.content }}
        </div>
      </div>
      <div class="2xl:w-sm flex flex-col gap-4">
        <UCard variant="soft" color="primary" class="w-full 2xl:flex-none">
          <template #header>
            <h2 class="font-bold text-md">
              Objavio
            </h2>
            <UUser
              :avatar="{ src: 'https://github.com/benjamincanac.png' }"
              name="John Doe"
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
        <UButton size="xl" class="h-12" color="primary" variant="solid" block>
          <UIcon name="i-solar:chat-round-line-outline" class="size-7 mr-2" />
          Započni razgovor
        </UButton>
        <UButton size="xl" class="h-12" color="secondary" variant="solid" block>
          <UIcon name="i-iconoir:donate" class="size-7 mr-2" />
          Pošalji zahtjev za donaciju
        </UButton>
      </div>
    </div>
  </RegisteredUserLayout>
</template>

<style scoped>

</style>
