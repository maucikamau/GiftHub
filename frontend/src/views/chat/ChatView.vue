<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeConversationId = computed(() => route.params.id as string)
</script>

<template>
  <div class="flex gap-4 w-full h-full">
    <div class="flex-col">
      <h2 class="font-medium text-2xl flex-1 text-neutral-900 mb-4">
        Nedavni razgovori
      </h2>
      <div class="d-flex flex-col gap-2 w-80">
        <ChatRecents :active-conversation-id="activeConversationId" />
      </div>
    </div>
    <RouterView class="w-full max-w-[1400px] mx-auto h-full flex flex-col gap-4" />
  </div>
</template>

<style scoped></style>
