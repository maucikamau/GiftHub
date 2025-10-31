<script setup lang="ts">
</script>

<template>
  <div class="flex min-h-screen">
    <div class="w-[40%]">
      <img src="/PlayForward_Banner.png" class="banner-img" />
    </div>
    <div class="w-[60%] flex items-center justify-center">
      <div class="p-[2px] bg-gradient-to-r from-[#f9b233] to-[#ef4fa6] rounded-2xl">
        <div class="bg-white rounded-2xl p-6 text-center">
          <div class="max-w-md text-center px-4">
            <h1 class="logo-text m-4 text-6xl">PlayForward</h1>
            <hr style="color: gray">
            <p class="font-bold m-4" style="font-family: 'Comfortaa'">
              Da biste pristupili platformi, morate se prijaviti.
            </p>
            <RouterLink to="/registracija"
              class="block text-black text-center py-2 px-6 border-1 hover:bg-gray-200 shadow-sm mb-3"
              style="font-family: 'Comfortaa'">
              <img src="/Google_Favicon_2025.png" class="favicon" />Prijava s Google računom
            </RouterLink>
            <RouterLink to="/registracija"
              class="block text-black text-center py-2 px-6 border-1 hover:bg-gray-200 shadow-sm mb-3"
              style="font-family: 'Comfortaa'">
              <img src="/Microsoft_icon.png" class="favicon" />Prijava sa Microsoft računom
            </RouterLink>
            <RouterLink to="/registracija"
              class="block text-black text-center py-2 px-6 border-1 hover:bg-gray-200 shadow-sm mb-3"
              style="font-family: 'Comfortaa'">
              <img src="/Apple_logo_black.png" class="favicon" />Prijava s Apple računom
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
