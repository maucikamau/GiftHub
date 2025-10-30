<script setup lang="ts">
</script>

<template>
  <div class="flex min-h-screen">
    <div class="w-[40%] bg-rainbow"></div>
    <div class="w-[60%] flex items-center justify-center">
      <div class="max-w-md text-center px-4">
        <h1 class="text-6xl m-4" style="font-family: 'Cherry Bomb One', cursive; color: #ED7474;">PlayForward</h1>
        <hr style="color: gray">
        <p class="font-bold m-4" style="font-family: 'Comfortaa'">
          Prijavi se za pregled oglasa:
        </p>
        <RouterLink
          to="/registracija"
          class="block bg-[#ED7474] text-black text-center py-4 px-6 rounded-xl border-1 hover:bg-gray-200" style="font-family: 'Comfortaa'"
          >Google prijava</RouterLink
        >
      </div>
    </div>
  </div>
</template>

