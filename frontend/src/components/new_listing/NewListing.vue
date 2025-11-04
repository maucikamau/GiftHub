<script setup lang="ts">
</script>

<template>
    <div class="flex h-screen">
        <div class="w-3/5">
            <div class="flex flex-col justify-between">
                <p class="text-xs mb-4">Oglasi / <span class="text-orange-400">Objavi novi oglas</span></p>
                <UInput class="w-full mb-4" placeholder="Unesite naziv igračke" />
                <UFileUpload accept="image/*,png/*,jpg/*" label="Dodaj ručno ili povuci slike koje želiš objaviti uz oglas." multiple class="min-h-48 cursor-pointer mb-4" />
                <!--<UTextarea :rows="12" placeholder="Type something..." />-->
            </div>
        </div>
        <div class="w-2/5">

        </div>
    </div>
</template>

<style scoped></style>