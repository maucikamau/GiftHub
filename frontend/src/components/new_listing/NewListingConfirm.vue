<script setup lang="ts"></script>

<template>
    <div class="flex flex-col">
        <p class="text-xs mb-4">Oglasi / Objavi novi oglas / <span class="text-orange-400">Potvrda</span></p>
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
                Title
                </h3>
                <h4 class="font-medium text-md text-stone-700">
                Mjesto
                </h4>
            </div>
            <p class="text-md font-medium text-stone-700 my-2 h-20">
                Description
            </p>
            <div class="flex gap-4">
                <span class="font-medium text-stone-400">Condition</span>
                <span class="font-medium text-stone-400">Category</span>
                <span class="font-medium text-stone-400">Delivery</span>
            </div>
            </div>
        </div>
        </UCard>
        <div class="flex justify-between text-center mt-6">
            <RouterLink
                to="/oglasi/novi"
                class="text-white font-bold py-2 px-4 bg-orange-500 hover:bg-orange-700 cursor-pointer rounded-full max-w-sm transition-colors col-span-2 return-button"
                >
                <p>← Natrag</p>
            </RouterLink>
            <RouterLink
                to="/"
                class="text-white font-bold py-2 px-4 bg-green-500 hover:bg-green-700 cursor-pointer rounded-full max-w-sm transition-colors col-span-2 return-button"
                >
                <p>Objavi</p>
            </RouterLink>
        </div>
    </div>
</template>