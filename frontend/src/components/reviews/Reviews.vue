<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { User } from '@/types/user'
import type { Review } from '@/types/reviews'
import { api } from '@/lib/apiClient'

interface Props {
  donor: User | null
  userId: number
}

const props = defineProps<Props>()

const reviews = ref<Review[]>([])
const loading = ref(true)

onMounted(async () => {
  const res = await api(`/api/reviews/list/${props.userId}`)
  reviews.value = await res.json()
  loading.value = false
})
</script>

<template>
  <div>
    <h1 class="text-2xl font-semibold mb-4">Recenzije za {{ props.donor?.username }}</h1>

    <UEmpty
      v-if="reviews?.length === 0"
      icon="i-tabler-alert-square-rounded"
      title="Nema dostupnih recenzija."
      description="Trenutno nema dostupnih recenzija za prikaz."
      :ui="{ body: 'max-w-full' }"
    />

    <div v-else class="flex flex-col gap-4">
      <UCard v-for="review in reviews" :key="review.id">
        <p class="font-medium">Ocjena: ⭐ {{ review.rating }}/5</p>
        <p>{{ review.comment || 'Bez komentara' }}</p>
      </UCard>

    </div>
  </div>
</template>