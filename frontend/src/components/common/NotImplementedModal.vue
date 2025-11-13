<script setup lang="ts">
const {
  message = 'Ova funkcionalnost je još u razvoju i trenutno nije dostupna.',
} = defineProps<{
  message?: string
}>()
</script>

<template>
  <UModal title="U razvoju">
    <template #body>
      <p>{{ message }}</p>
    </template>
    <template #footer="{ close }">
      <div class="w-full flex justify-end">
        <UButton label="Zatvori" color="neutral" @click="close" />
      </div>
    </template>
  </UModal>
</template>
