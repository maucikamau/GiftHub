<script setup lang="ts">
import { useRoute } from 'vue-router'
import Reviews from '@/components/reviews/Reviews.vue'

const route = useRoute()
const userId = Number(route.params.userId)
</script>

<template>
  <Reviews :user-id="userId" />
</template>
