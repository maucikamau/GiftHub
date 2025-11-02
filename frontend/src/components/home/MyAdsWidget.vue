<template>
  <div class="flex">
    <h2 class="font-medium text-2xl flex-1 text-neutral-900 mt-8 mb-4">
      Moji oglasi
    </h2>
    <UButton
      :ui="{ base: 'px-4 py-2 text-base', leadingIcon: 'size-6' }"
      variant="solid"
      color="primary"
      icon="i-lucide:plus"
      to="/oglasi/novi"
      class="mt-6 mb-4"
    >
      Novi oglas
    </UButton>
  </div>
  <div class="flex flex-col">
    <UCard>
      <div class="flex gap-6">
        <div class="w-40">
          <div
            class="w-40 aspect-[16/9] bg-gradient-to-t from-neutral-800 to-neutral-50 rounded-lg"
          />
        </div>
        <div class="flex-1 flex flex-col">
          <div class="flex gap-4 items-end">
            <h3 class="font-bold text-2xl text-stone-900">
              Oglas 1
            </h3>
            <h4 class="font-medium text-md text-stone-700">
              Mjesto
            </h4>
          </div>
          <p class="text-md font-medium text-stone-700 my-2 h-20">
            Kratak opis
          </p>
          <div class="flex gap-4">
            <span class="font-medium text-stone-400">Novo</span>
            <span class="font-medium text-stone-400">Plišanac</span>
            <span class="font-medium text-stone-400">Osobno preuzimanje</span>
          </div>
        </div>
      </div>
    </UCard>
  </div>
</template>
