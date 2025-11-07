<script setup lang="ts">
import { ref } from 'vue'

const cities = ref([
  { label: 'Zagreb', value: 'zagreb' },
  { label: 'Split', value: 'split' },
  { label: 'Rijeka', value: 'rijeka' },
  { label: 'Osijek', value: 'osijek' },
  { label: 'Zadar', value: 'zadar' },
])
</script>

<template>
  <form class="grid grid-cols-2 gap-4 mb-4">
    <div class="flex justify-start flex-col">
      <p class="m-1 font-semibold">
        Ime
      </p>
      <UInput placeholder="Unesite ime" />
    </div>
    <div class="flex flex-col">
      <p class="m-1 font-semibold">
        Prezime
      </p>
      <UInput placeholder="Unesite prezime" />
    </div>
    <div class="flex flex-col">
      <p class="m-1 font-semibold">
        Korisničko ime
      </p>
      <UInput placeholder="Unesite korisničko ime" />
      <p class="m-1 text-xs">
        Tvoje korisničko ime je <span class="font-semibold">javno</span> i bit će korišteno za
        komunikaciju sa drugima u chatu.
      </p>
    </div>
    <div class="flex flex-col">
      <p class="m-1 font-semibold">
        Mjesto
      </p>
      <USelectMenu :items="cities" placeholder="Odaberite mjesto" />
      <p class="m-1 text-xs">
        Koristimo mjesto za lakši pronalazak oglasa u tvom mjestu.
        Uvijek možeš promijeniti mjesto za pojedinačne oglase.
      </p>
    </div>

    <div class="flex items-center col-span-2 my-4">
      <UCheckbox
        size="lg"
        label="Potvrđujem da sam punoljetna osoba i slažem se s Uvjetima korištenja."
      />
    </div>
  </form>
</template>
