<script setup lang="ts">
</script>

<template>
    <div class="flex items-center justify-center min-h-screen bg-rainbow">
        <div class="p-8 bg-white text-center h-150 w-150 rounded-xl shadow-lg">
            <h1 class="text-6xl m-4" style="font-family: 'Cherry Bomb One', cursive; color: #A7C7F7;">PlayForward</h1>
            <br>
            <p class="font-bold text-xl m-4" style="font-family: 'Comfortaa'">
                Pozdrav! Vrijeme da se upozamo:
            </p>
            <p class="m-4" style="font-family: 'Comfortaa'">
                Prijavljen si kao: <span class="font-bold italic">xyz@hotmail.com</span>
            </p>
            <br>
            <p class="font-bold text-xl m-4 text-left" style="font-family: 'Comfortaa'">
                Koristim platformu kao...
            </p>
            <div class="flex h-[30%] text-center">
                <RouterLink
                    to="/registracija/privatni_korisnik"
                    class="w-1/2 flex m-1 items-center justify-center rounded-xl bg-[#A7C7F7] hover:bg-gray-200" style="font-family: 'Comfortaa'"
                    >Privatni korisnik</RouterLink
                >
                <RouterLink
                    to="/registracija/udruga"
                    class="w-1/2 flex m-1 items-center justify-center rounded-xl bg-[#A7C7F7] hover:bg-gray-200" style="font-family: 'Comfortaa'"
                    >Udruga</RouterLink
                >
            </div>
        </div>
    </div>
</template>