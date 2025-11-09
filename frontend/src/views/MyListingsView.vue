<script setup lang="ts">
import { storeToRefs } from 'pinia'
import RegisteredUserLayout from '@/layouts/RegisteredUserLayout.vue'
import { useUserStore } from '@/stores/user.ts'

const store = useUserStore()
const { user } = storeToRefs(store)
</script>

<template>
  <RegisteredUserLayout v-if="user">
    <MyListingsWidget />
  </RegisteredUserLayout>
</template>
