<script setup lang="ts">
</script>

<template>
    <div class="flex items-center justify-center min-h-screen bg-rainbow">
        <div class="p-8 bg-white text-center h-150 w-150 rounded-xl shadow-lg">
            <h1 class="text-6xl m-4">PlayForward</h1>
            <br>
            <p class="font-bold text-xl m-4">
                Pozdrav! Vrijeme da se upoznamo.
            </p>
            <p class="m-4">
                Prijavljen si kao: <span class="font-bold italic">xyz@hotmail.com</span>
            </p>
            <br>
            <p class="font-bold text-xl m-4 text-left">
                Ja sam...
            </p>
            <div class="flex h-[30%] text-center">
                <RouterLink
                    to="/registracija/donator"
                    class="w-1/2 flex m-1 items-center justify-center rounded-xl bg-[#B5EAD7] hover:bg-gray-200"
                    >Donator</RouterLink
                >
                <RouterLink
                    to="/registracija/primatelj"
                    class="w-1/2 flex m-1 items-center justify-center rounded-xl bg-[#A7C7F7] hover:bg-gray-200"
                    >Primatelj</RouterLink
                >
            </div>
        </div>
    </div>
</template>

