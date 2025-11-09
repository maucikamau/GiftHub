<script setup lang="ts">
import { storeToRefs } from 'pinia'
import RegisteredUserLayout from '@/layouts/RegisteredUserLayout.vue'
import { useUserStore } from '@/stores/user.ts'
import HomeDonorView from '@/views/home/HomeDonorView.vue'
import HomeRecipientView from '@/views/home/HomeRecipientView.vue'

const store = useUserStore()
const { user } = storeToRefs(store)
</script>

<template>
  <RegisteredUserLayout v-if="user">
    <h1 class="font-medium text-4xl text-neutral-900">
      Pozdrav, {{ user.first_name }}! 👋
    </h1>
    <HomeDonorView v-if="user.role === 'donor'" />
    <HomeRecipientView v-else />
  </RegisteredUserLayout>
</template>
