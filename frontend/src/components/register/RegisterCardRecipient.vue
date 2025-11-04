<script setup lang="ts">
import Logo from '@/assets/PlayForward_Logo.svg'
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-brand-gradient-soft">
    <div class="p-8 bg-white text-left h-150 w-150 rounded-xl shadow-lg space-y-21.5">
      <img :src="Logo" class="logo">
      <br>
      <p class="font-bold text-xl m-4">
        Drago nam je što si ovdje.
      </p>
      <p class="m-4">
        Prijavljen si kao: <span class="font-bold italic">xyz@hotmail.com</span>
      </p>
      <br>
      <p class="font-bold text-xl m-4 text-left">
        Koristim platformu kao...
      </p>
      <div class="flex h-[30%]">
        <RouterLink
          to="/registracija/privatniKorisnik"
          class="button w-1/2 m-1 rounded-xl"
        >
          <p>Privatni korisnik</p>
          <img src="/static/primatelj2.png"></img>
        </RouterLink>
        <RouterLink
          to="/registracija/udruga"
          class="button w-1/2 m-1 rounded-xl"
        >
          <p>Udruga</p>
          <img src="/static/primatelj.png"></img>
        </RouterLink>
      </div>
      <RouterLink
        to="/registracija"
        class="return-button my-8"
      >
        <p>← Natrag</p>
      </RouterLink>
    </div>
  </div>
</template>
