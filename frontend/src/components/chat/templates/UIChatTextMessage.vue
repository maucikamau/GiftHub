<script setup lang="ts">
import type { ChatMessage } from '@/types/chat.ts'
import { computed } from 'vue'
import { chatClient, isChatClientReady } from '@/lib/streamChat.ts'
import { formatTimestamp } from '@/utils/time.ts'

const { message } = defineProps<{
  message: ChatMessage
}>()

const isOwn = computed(() => isChatClientReady.value && message.from.chat_uid === chatClient.userID)
</script>

<template>
  <div
    class="flex gap-2" :class="[
      isOwn ? 'justify-end' : 'justify-start',
    ]"
  >
    <UAvatar
      v-if="!isOwn"
      :src="message.from.username"
      :alt="message.from.username"
      size="xs"
      class="mt-auto mb-1"
    />

    <div class="flex flex-col max-w-[65%] group" :class="[isOwn ? 'items-end' : 'items-start']">
      <div class="flex items-end gap-2">
        <!-- Edit button -->
        <UButton
          v-if="isOwn"
          icon="i-lucide:pencil"
          size="sm"
          color="neutral"
          variant="solid"
          class="mt-1 opacity-0 group-hover:opacity-100"
        />
        <div
          class="relative px-3 py-2 rounded-lg shadow-sm" :class="[
            isOwn
              ? 'bg-surface-500 text-white rounded-br-sm'
              : 'bg-white text-neutral-900 rounded-bl-sm',
          ]"
        >
          <div class="flex items-end gap-2">
            <p class="text-sm whitespace-pre-wrap break-words">
              {{ message.content }}
            </p>
            <span
              class="text-[10px] leading-none whitespace-nowrap" :class="[
                isOwn ? 'text-white/70' : 'text-neutral-500',
              ]"
            >
              {{ formatTimestamp(message.createdAt) }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
