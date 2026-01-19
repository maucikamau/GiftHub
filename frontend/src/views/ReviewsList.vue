<script setup lang="ts">
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import { getUserById } from '@/api/user'
import Reviews from '@/components/reviews/Reviews.vue'
import type { User } from '@/types/user'

const route = useRoute()
const userId = Number(route.params.userId)

const donor = ref<User | null>(null)

onMounted(async () => {
  try {
    donor.value = await getUserById(userId)
  } catch (error) {
    console.error('Error fetching user:', error)
  }
})
</script>

<template>
  <Reviews :donor="donor" :userId="userId" />
</template>

<style scoped></style>