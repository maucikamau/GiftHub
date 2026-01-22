<script setup lang="ts">
import type { TemporaryChatConversation } from '@/types/chat.ts'
import { useRoute, useRouter } from 'vue-router'
import { createChat } from '@/api/chat.ts'
import { useGetListing } from '@/services/listings.ts'
import { useGetUserAvgReviews } from '@/services/reviews.ts'
import { useGetCurrentUser } from '@/services/user.ts'
import { formatText } from '@/utils/formatting.ts'
import { useModal } from '@/utils/modal.ts'

const route = useRoute('pregled-oglasa')
const { data: user } = useGetCurrentUser()

const { showNotImplementedModal, showDonationRequestModal } = useModal()
const toast = useToast()
const router = useRouter()

const {
  data: listing,
  isLoading,
  error,
} = useGetListing(() => Number(route.params.id))

async function startConversation() {
  if (!user.value || !listing.value)
    return

  if (!listing.value.owner.chat_uid) {
    console.error('Owner does not have a chat UID')
  }

  const chatStatus = await createChat(listing.value.id).catch((err) => {
    toast.add({
      title: 'Greška pri pokretanju razgovora',
      description: err.message || 'Došlo je do greške pri pokretanju razgovora.',
      color: 'error',
    })
    return null
  })

  if (!chatStatus)
    return

  router.push({ name: 'aktivan-razgovor', params: { id: chatStatus.stream_channel_id } })
}

function requestDonation() {
  if (!user.value || !listing.value)
    return

  if (!listing.value.owner.chat_uid) {
    console.error('Owner does not have a chat UID')
    return
  }

  const conversation: TemporaryChatConversation = {
    receiver: listing.value.owner,
    listing: { id: listing.value.id, title: listing.value.title, picture: listing.value.picture || '' },
  }
  showDonationRequestModal(conversation)
}

const { data: reviewData, isInitialLoading: fetchingAvg } = useGetUserAvgReviews(() => listing.value?.owner.id)
</script>

<template>
  <USkeleton v-if="isLoading" class="w-full h-40" />
  <UEmpty
    v-if="error && error.message.includes('404')"
    title="Oglas nije pronađen"
    description="Oglas koji tražite ne postoji ili je uklonjen."
    icon="i-tabler:search-off"
  />
  <UEmpty
    v-else-if="error && error.message.includes('403')"
    title="Oglas više nije dostupan"
    description="Oglas koji tražite više nije dostupan za donaciju."
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
            class="w-full mt-3 mb-1"
            :ui="{ name: 'text-2xl font-semibold', avatar: 'size-14' }"
            :avatar="{ src: listing.owner.profile_image || '/static/default_profile_pic.png' }"
          />
          <div v-if="fetchingAvg" class="flex">
            <USkeleton class="w-32 h-8" />
          </div>
          <div v-else-if="reviewData?.total === 0" class="text-sm text-neutral-600">
            Još nema recenzija!
          </div>
          <div v-else class="flex">
            <div class="text-2xl font-medium gap-2 flex items-end">
              <span class="text-6xl">{{ reviewData?.average || 0 }}</span>/5
            </div>
            <div class="flex flex-col ml-4">
              <Stars :stars="reviewData?.stars || 0" size="lg" />
              <UButton variant="ghost" trailing-icon="i-tabler:arrow-right" size="sm" class="mt-1" :to="{ name: 'recenzije', params: { userId: listing.owner.id } }">
                Pogledaj {{ formatText(reviewData?.total || 0, 'recenzija') }}
              </UButton>
            </div>
          </div>
        </template>
      </UCard>

      <template
        v-if="listing.owner.id !== user?.id && listing.status === 'available'"
      >
        <UButton size="xl" class="h-12" color="primary" variant="solid" block @click="startConversation">
          <UIcon name="i-solar:chat-round-line-outline" class="size-7 mr-2" />
          Započni razgovor
        </UButton>
        <UButton size="xl" class="h-12" color="secondary" variant="solid" block @click="requestDonation">
          <UIcon name="i-lucide:hand-heart" class="size-7 mr-2" />
          Pošalji zahtjev za donaciju
        </UButton>
      </template>
      <template v-else-if="listing.owner.id === user?.id">
        <UButton leading-icon="i-lucide:pencil" size="xl" class="h-12" color="primary" variant="solid" block :to="`/oglasi/${listing.id}/uredi`">
          Uredi oglas
        </UButton>
        <UButton leading-icon="i-lucide:trash" size="xl" class="h-12" color="error" variant="solid" block @click="showNotImplementedModal()">
          Obriši oglas
        </UButton>
      </template>
      <UButton v-if="listing.conversation_id" leading-icon="i-solar:chat-round-line-outline" size="xl" class="h-12" color="secondary" variant="solid" block :to="{ name: 'aktivan-razgovor', params: { id: listing.conversation_id } }">
        Otvori aktivan razgovor
      </UButton>
    </div>
  </div>
</template>
