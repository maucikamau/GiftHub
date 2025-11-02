<script setup lang="ts">
import { storeToRefs } from 'pinia'
import MyAdsWidget from '@/components/home/MyAdsWidget.vue'
import RegisteredUserLayout from '@/layouts/RegisteredUserLayout.vue'
import { useUserStore } from '@/stores/user.ts'

const store = useUserStore()
const { user } = storeToRefs(store)
</script>

<template>
  <RegisteredUserLayout>
    <h1 class="font-medium text-4xl text-neutral-900">
      Dobrodošao, {{ user.firstName }}! 👋
    </h1>
    <MyAdsWidget />
  </RegisteredUserLayout>
</template>
