<script setup lang="ts">
import type { ChatConversation } from '@/lib/streamChat.ts'
import { useGetRecentConversations } from '@/services/conversation.ts'

const activeConversation = defineModel<ChatConversation | null>({ required: true })

const { data: recentConversations, isInitialLoading } = useGetRecentConversations()
</script>

<template>
  <template v-if="isInitialLoading">
    <USkeleton
      v-for="n in 5"
      :key="n"
    />
  </template>
  <template v-for="page in recentConversations?.pages" :key="page.nextPage">
    <UButton
      v-for="conversation in page"
      :key="conversation.id"
      :variant="activeConversation?.id === conversation.id ? 'soft' : 'ghost'"
      color="surface"
      class="text-left px-4 py-2 w-full"
      trailing-icon="i-oui:arrow-right"
      @click="activeConversation = conversation"
    >
      <UUser
        :name="conversation.user.name"
        :description="conversation.listing.title"
        :avatar="{ src: conversation.user.avatar }"
        :chip="{
          color: conversation.user.online ? 'success' : 'surface',
          position: 'top-right',
        }"
        class="w-full"
      />
    </UButton>
  </template>
</template>

<style scoped>

</style>
