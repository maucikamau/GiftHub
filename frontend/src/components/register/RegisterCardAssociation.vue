<script setup lang="ts">
import Logo from '@/assets/PlayForward_Logo.svg'
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-brand-gradient-soft">
    <div class="p-8 bg-white text-left h-160 w-150 rounded-xl shadow-lg">
      <img :src="Logo" class="logo">
      <br>
      <p class="font-bold text-xl m-4">
        Još samo kratko o udruzi 💕
      </p>
      <p class="m-4">
        Prijavljen si kao: <span class="font-bold italic">xyz@hotmail.com</span>
      </p>
      <br>
      <form class="text-left">
        <p class="m-4 font-semibold">
          Ime udruge
        </p>
        <input
          class="ml-4"
          placeholder="Unesite naziv udruge"
        >
        <br>
        <p class="m-4 font-semibold">
          E-mail udruge
        </p>
        <input
          class="ml-4"
          placeholder="Unesite e-mail"
        >
        <br>
        <button class="ml-4 register-btn bg-brand-gradient" type="submit">
          Registriraj se
        </button>
      </form>
      <RouterLink
        to="/registracija/primatelj"
        class="return-button m-1"
      >
        <p>← Natrag</p>
      </RouterLink>
    </div>
  </div>
</template>
