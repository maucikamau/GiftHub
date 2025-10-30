<script setup lang="ts">
import LoginLayout from "@/layouts/LoginLayout.vue";
</script>

<template>
  <LoginLayout>
    <div class="h-full grid place-items-center">
      <div class="w-full max-w-[600px] mx-auto px-4 py-2">
        <h1 class="font-bold text-2xl">You did it!</h1>
        <p>
          Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read
          the
          documentation
        </p>
      </div>
    </div>
  </LoginLayout>
</template>

<style scoped></style>

<!--
<script setup>
import LeftHome from '@/components/LeftHome.vue';
import RightHome from '@/components/RightHome.vue';
</script>

<template>
  <LeftHome />
  <RightHome />
</template>
-->
