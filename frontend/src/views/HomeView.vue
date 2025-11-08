<script setup lang="ts">
import { storeToRefs } from 'pinia'
import MyListingsWidget from '@/components/home/MyListingsWidget.vue'
import RegisteredUserLayout from '@/layouts/RegisteredUserLayout.vue'
import { useUserStore } from '@/stores/user.ts'

const store = useUserStore()
const { user } = storeToRefs(store)
</script>

<template>
  <RegisteredUserLayout>
    <h1 class="font-medium text-4xl text-neutral-900">
      Pozdrav, {{ user?.first_name }}! 👋
    </h1>
    <MyListingsWidget />
  </RegisteredUserLayout>
</template>
