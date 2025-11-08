<script setup lang="ts">
import { onMounted } from 'vue'
import { logout } from '@/api/user.ts'
import CardLayout from '@/layouts/CardLayout.vue'
import { useUserStore } from '@/stores/user.ts'

const userStore = useUserStore()

onMounted(() => {
  logout()
  userStore.user = undefined
})
</script>

<template>
  <CardLayout>
    <div class="grid place-items-center h-full">
      <UCard variant="outline" class="px-8 py-4 shadow-md text-center m-4 w-full max-w-md">
        <h1 class="text-2xl font-medium mt-4">
          Vidimo se uskoro! ✌
        </h1>
        <p class="mt-2 text-surface-100">
          Uspješno ste se odjavili.
        </p>
        <UButton
          to="/prijava" class="mt-6" icon="i-material-symbols:login" color="primary"
          variant="soft" size="xl"
        >
          Idi na prijavu
        </UButton>
      </UCard>
    </div>
  </CardLayout>
</template>

<style scoped>

</style>
