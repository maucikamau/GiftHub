<script setup lang="ts">
    import Logo from '@/assets/PlayForward_Logo.svg'
</script>

<template>
    <div class="flex items-center justify-center min-h-screen bg-brand-gradient-soft">
        <div class="p-8 bg-white text-left h-160 w-150 rounded-xl shadow-lg">
            <img :src="Logo" class="logo">
            <br>
            <p class="font-bold text-xl m-4">
                Još samo malo i gotovo!
            </p>
            <p class="m-4">
                Prijavljen si kao: <span class="font-bold italic">xyz@hotmail.com</span>
            </p>
            <form class="grid grid-cols-2 mb-4">
                <div>
                    <p class="m-2 font-semibold">Ime</p>
                    <UInput class="!w-56 ml-2" placeholder="Unesite ime" />
                </div>
                <div>
                    <p class="m-2 font-semibold">Prezime</p>
                    <UInput class="!w-56 ml-2" placeholder="Unesite prezime" />
                </div>
                <div>
                    <p class="m-2 font-semibold">Korisničko ime</p>
                    <UInput class="!w-56 ml-2" placeholder="Unesite korisničko ime" />
                </div>
                <div>
                    <p class="m-2 font-semibold">Mjesto</p>
                    <USelect class="!w-56 h-10 ml-2" placeholder="Unesite mjesto" />
                </div>
                <div>
                    <p class="m-2 text-xs">Tvoje korisničko ime je <span class="font-semibold">javno</span> i bit će korišteno za komunikaciju sa drugima u chatu.</p>
                </div>
                <div>
                    <p class="m-2 text-xs">Koristimo mjesto za filtriranje oglasa. Ovo ćemo mjesto koristiti kod objave novih oglasa. Uvijek možeš promijeniti mjesto za pojedinačne oglase.</p>
                </div>
            
            <div class="flex items-center col-span-2 mb-0">
                <UCheckbox size="lg" class="m-4" />
                <label class="flex-1 m-0 text-xs">Potvrđujem da sam punoljetna osoba i slažem se s Uvijetima korištenja.</label>
            </div>
            <UButton class="col-span-2 justify-center ml-4 register-btn bg-brand-gradient !mt-3 mb-4" type="submit">Registriraj se</UButton>
            <RouterLink
                    to="/registracija/primatelj"
                    class="col-span-2 return-button mt-2"
                    >
                    <p>← Natrag</p>
                </RouterLink>
            </form>
        </div>
    </div>
</template>