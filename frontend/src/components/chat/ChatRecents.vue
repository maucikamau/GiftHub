<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useGetRecentConversations } from '@/services/conversation.ts'

const { activeConversationId } = defineProps<{
  activeConversationId?: string
}>()

const router = useRouter()
const { data: recentConversations, isInitialLoading } = useGetRecentConversations()
</script>

<template>
  <template v-if="isInitialLoading">
    <USkeleton
      v-for="n in 5"
      :key="n"
    />
  </template>
  <div class="flex flex-col gap-0.5 -ml-4">
    <template v-for="(page, idx) in recentConversations?.pages" :key="idx">
      <UButton
        v-for="conversation in page"
        :key="conversation.id"
        :variant="activeConversationId === conversation.id ? 'soft' : 'ghost'"
        color="surface"
        class="text-left px-4 py-2 w-full"
        trailing-icon="i-oui:arrow-right"
        @click="router.push({ name: 'aktivan-razgovor', params: { id: conversation.id } })"
      >
        <UUser
          :name="conversation.listing.title"
          :description="conversation.receiver.username"
          :avatar="{ src: conversation.receiver.profile_image || '/static/default_profile_pic.png' }"
          :chip="{
            color: conversation.receiver.online ? 'success' : 'surface',
            position: 'top-right',
          }"
          :ui="{
            wrapper: 'min-w-0',
            name: 'overflow-hidden text-ellipsis',
            root: 'min-w-0',
          }"
          class="w-full"
        />
      </UButton>
    </template>
  </div>
</template>

<style scoped>

</style>
