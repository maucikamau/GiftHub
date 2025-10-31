<script setup lang="ts">
</script>

<template>
  <div class="bg-amber-300 blur-[200px] -z-10 size-100 fixed top-20 left-1/2 transform -translate-x-1/2" />
  <div class="bg-pink-300 blur-[200px] -z-10 size-100 fixed bottom-20 left-1/2 transform -translate-x-[100%]" />
  <div class="bg-rose-300 blur-[200px] -z-10 size-100 fixed bottom-20 left-1/2 transform translate-x-[20%]" />
  <div class="h-screen w-full">
    <slot />
  </div>
</template>
