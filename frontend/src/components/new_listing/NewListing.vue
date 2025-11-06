<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
// import axios from 'axios';

const lista_kategorija = ref(['Plišanci', 'Auti', 'Lutke'])
const lista_stanja = ref(['Rabljeno', 'Novo'])
const lista_dostava = ref(['Osobno preuzimanje', 'Dostava o trošku primatelja'])

const title = ref('')
const images = ref<File[]>([])
const description = ref('')
const category = ref('')
const condition = ref('')
const delivery = ref('')

const checklist = computed(() => [
    { label: 'Naslov', done: title.value.trim().length > 0 },
    { label: 'Slike', done: images.value.length > 0 },
    { label: 'Opis', done: description.value.trim().length > 0 },
    { label: 'Kategorija', done: !!category.value },
    { label: 'Stanje', done: !!condition.value },
    { label: 'Dostava', done: !!delivery.value },
])

const isComplete = computed(() => checklist.value.every(i => i.done))
const router = useRouter();

const handleSubmit = async () => {

    if (!isComplete.value) return

    const newListing = {
        title: title.value,
        images: images.value,
        description: description.value,
        category: category.value,
        condition: condition.value,
        delivery: delivery.value,
    };

    console.log(newListing)
    router.push('/oglasi/novi/potvrda');

    /*
    try {
        const response = await axios.post('/', newListing);
        router.push(`/oglas/${response.data.id}`);
    } catch (error) {
        console.error('Error fetching listing', error);
    }
    */
};


</script>

<template>
    <form @submit.prevent="handleSubmit">
        <div class="flex h-screen">
            <div class="w-3/5 mr-32">
                    <div class="flex flex-col justify-between">
                        <p class="text-xs mb-4">Oglasi / <span class="text-orange-400">Objavi novi oglas</span> / Potvrda</p>
                        <h2>Naslov:</h2>
                        <UInput v-model="title" class="w-full mb-4" placeholder="Unesite naziv igračke" />
                        <h2>Slike (minimalno 1 slika):</h2>
                        <UFileUpload v-model="images" accept="image/*,png/*,jpg/*" label="Dodajte ručno ili povucite slike koje želite objaviti uz oglas" multiple class="min-h-48 cursor-pointer mb-4" />
                        <h2>Opis:</h2>
                        <UTextarea v-model="description" :rows="8" class="mb-4" placeholder="Unesite opis igračke" />
                        <h2>Kategorija:</h2>
                        <USelect v-model="category" :items="lista_kategorija" class="w-56 h-10 mb-4" placeholder="Odaberite kategoriju" />
                        <h2>Stanje:</h2>
                        <URadioGroup v-model="condition" class="mb-4" orientation="horizontal" variant="card" default-value="" :items="lista_stanja" />
                        <h2>Dostava:</h2>
                        <URadioGroup v-model="delivery" orientation="horizontal" variant="card" default-value="" :items="lista_dostava" />
                    </div>
            </div>
            <div class="w-2/5">
                <aside class="sticky top-6">
                    <h3 class="text-lg mb-3">Provjera</h3>
                    <ul class="space-y-2">
                        <li v-for="item in checklist" :key="item.label" class="flex items-center justify-between p-3 border border-gray-200 rounded">
                            <span>{{ item.label }}</span>
                            <span v-if="item.done" class="text-green-600 font-bold">✓</span>
                            <span v-else class="text-gray-400">—</span>
                        </li>
                    </ul>
                    <div class="mt-8 flex justify-center text-center">
                        <button
                            type="submit"
                            class="text-white font-bold py-2 px-4 rounded-full w-full max-w-sm transition-colors"
                            :class="isComplete ? 'bg-green-500 hover:bg-green-700 cursor-pointer' : 'bg-green-200 cursor-not-allowed pointer-events-none'"
                            :disabled="!isComplete">
                            Pregledaj i objavi oglas
                        </button>
                    </div>
                </aside>
            </div>
        </div>
    </form>
</template>

<style scoped></style>