<script setup lang="ts">
import LoginLayout from "@/layouts/LoginLayout.vue"
import Logo from "@/assets/PlayForward_Logo.svg"
</script>

<template>
  <LoginLayout>
    <template #preview>
      <img src="/PlayForward_Banner.png" alt="PlayForward Banner"
           class="h-full w-full object-cover"/>
    </template>
    <template #default>
      <div
        class="p-[3px] bg-gradient-to-r h-full max-w-[660px] w-full max-h-[720px] from-[#f9b233] to-[#ef4fa6] rounded-2xl">
        <div class="bg-white rounded-2xl h-full py-6 px-4 grid place-items-center">
          <div class="flex flex-col">
            <img :src="Logo" class="text-6xl h-16 w-min"/>
            <p class="font-medium text-lg pr-8 py-4">
              Da biste pristupili platformi, morate se prijaviti.
            </p>
            <UButton to="/registracija" variant="outline" color="neutral" block size="xl"
                     class="my-2" icon="i-logos:google-icon">
              Prijava s Google računom
            </UButton>
            <UButton to="/registracija" variant="outline" color="neutral" block size="xl"
                     class="my-2" icon="i-logos:microsoft-icon">
              Prijava s Microsoft računom
            </UButton>
            <UButton to="/registracija" variant="outline" color="neutral" block size="xl"
                     class="my-2" icon="i-logos:apple">
              Prijava s Apple računom
            </UButton>
          </div>
        </div>
      </div>
    </template>
  </LoginLayout>
</template>

<style scoped></style>
