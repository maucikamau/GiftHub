<script setup lang="ts">
import { useGetCurrentUser } from '@/services/user.ts'
import HomeDonorView from '@/views/home/HomeDonorView.vue'
import HomeRecipientView from '@/views/home/HomeRecipientView.vue'

const { data: user } = useGetCurrentUser()
</script>

<template>
  <template v-if="user">
    <h1 class="font-medium text-4xl text-neutral-900">
      Pozdrav, {{ user.first_name }}! 👋
    </h1>
    <HomeDonorView v-if="user.role === 'donor'" />
    <HomeRecipientView v-else />
  </template>
</template>
