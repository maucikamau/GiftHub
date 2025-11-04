<script setup>
import Logo from '@/assets/PlayForward_Logo.svg'
</script>

<template>
  <div
    class="main_container min-h-screen bg-[url(/static/PlayForward_Banner.png)] bg-center bg-no-repeat bg-cover"
  >
    <div class="hello bg-brand-gradient-softer" style="font-family: 'Montserrat';">
      <p class="block font-bold text-2xl text-[#69644F]">
        Zašto bi stare igračke skupljale prašinu?
      </p>
      <p class=" block text-lg text-[#968F70]">
        Podijeli svoje stare igračke i pomozi zajednici.
      </p>
    </div>
    <div class="grid [grid-area:login] place-items-center w-full h-full">
      <div
        class="p-[3px] bg-gradient-to-r h-full max-w-[660px] w-full max-h-[720px] from-[#f9b233] to-[#ef4fa6] rounded-2xl"
      >
        <div class="bg-white rounded-2xl h-full py-6 px-4 grid place-items-center">
          <div class="flex flex-col">
            <img :src="Logo" class="text-6xl h-16 w-min">
            <p class="font-medium text-lg pr-8 py-4">
              Da biste pristupili platformi, morate se prijaviti.
            </p>
            <UButton
              to="/registracija" variant="outline" color="neutral" block size="xl"
              class="my-2" icon="i-logos:google-icon"
            >
              Prijava s Google računom
            </UButton>
            <UButton
              to="/registracija" variant="outline" color="neutral" block size="xl"
              class="my-2" icon="i-logos:microsoft-icon"
            >
              Prijava s Microsoft računom
            </UButton>
            <UButton
              to="/registracija" variant="outline" color="neutral" block size="xl"
              class="my-2" icon="i-logos:apple"
            >
              Prijava s Apple računom
            </UButton>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
