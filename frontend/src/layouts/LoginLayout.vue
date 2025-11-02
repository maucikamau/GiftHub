<script setup>
  import Logo from '@/assets/PlayForward_Logo.svg'
</script>

<template>
  <div class="main_container min-h-screen bg-[url(/PlayForward_Banner.png)] bg-center bg-no-repeat bg-cover">
    <div class="hello" style="font-family: 'Montserrat';">
      <p class="block font-bold text-2xl text-[#69644F]">Zašto bi stare igračke skupljale prašinu?</p>
      <p class=" block text-lg text-[#968F70]">Podijeli svoje stare igračke i pomozi zajednici.</p>
    </div>
    <div class="login_container">
      <div class="p-[2px] bg-gradient-to-r from-[#F7FF00] to-[#DB36A4] rounded-2xl">
        <div class="bg-white rounded-2xl p-6">
          <div class="login max-w-md px-4">
            <div>
              <img :src="Logo" class="text-6xl h-12 w-min m-3 mb-4">
            </div>
            <p class="font-bold m-4 text-[#B6B096]" style="font-family: 'Montserrat'">
              Prijavite se da biste pristupili platformi.
            </p>
            <RouterLink to="/registracija"
              class="block text-black text-center py-2 px-6 border-1 border-[#DDDDDD] hover:bg-gray-200 shadow-sm mb-3"
              style="font-family: 'Montserrat'">
              <img src="/Google_Favicon_2025.png" class="favicon" />Prijava s Google računom
            </RouterLink>
            <RouterLink to="/registracija"
              class="block text-black text-center py-2 px-6 border-1 border-[#DDDDDD] hover:bg-gray-200 shadow-sm mb-3"
              style="font-family: 'Montserrat'">
              <img src="/Microsoft_icon.png" class="favicon" />Prijava sa Microsoft računom
            </RouterLink>
            <RouterLink to="/registracija"
              class="block text-black text-center py-2 px-6 border-1 border-[#DDDDDD] hover:bg-gray-200 shadow-sm mb-3"
              style="font-family: 'Montserrat'">
              <img src="/Apple_logo_black.png" class="favicon" />Prijava s Apple računom
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
