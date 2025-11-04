<script setup lang="ts">
import Logo from '@/assets/PlayForward_Logo.svg'
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-brand-gradient-soft">
    <div class="p-8 bg-white text-center h-160 w-150 rounded-xl shadow-lg">
      <img :src="Logo" class="logo">
      <br>
      <p class="font-bold text-xl m-4">
        Pozdrav! Vrijeme da se upoznamo.
      </p>
      <p class="m-4 mb-8">
        Prijavljen si kao: <span class="font-bold italic">xyz@hotmail.com</span>
      </p>
      <p class="font-bold text-xl m-4 text-left">
        Ja sam...
      </p>
      <div class="flex h-[30%]">
        <RouterLink
          to="/registracija/donator"
          class="button w-1/2 m-1 rounded-xl"
        >
          <p>Donator</p>
          <img src="/static/donator.png"></img>
        </RouterLink>
        <RouterLink
          to="/registracija/primatelj"
          class="button w-1/2 m-1 rounded-xl"
        >
          <p>Primatelj</p>
          <img src="/static/primatelj.png"></img>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
