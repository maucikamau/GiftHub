<script setup lang="ts">

</script>

<template>
  <div class="min-h-screen flex">
    <div class="flex-1">
      <slot name="preview" />
    </div>
    <div class="flex-1">
      <slot />
    </div>
  </div>
</template>

<style scoped>

</style>
