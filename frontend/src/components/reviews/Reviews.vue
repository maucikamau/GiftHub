<script setup lang="ts">
import { useGetUserReviews } from '@/services/reviews'

const { userId } = defineProps<{ userId: number }>()
const { data: reviewsData, isInitialLoading: loading } = useGetUserReviews(() => userId)
</script>

<template>
  <div>
    <h1 class="text-2xl font-semibold mb-4">
      Recenzije za {{ reviewsData?.donor?.username }}
    </h1>

    <USkeleton
      v-if="loading"
      class="w-full h-40"
    />

    <UEmpty
      v-else-if="!reviewsData?.reviews?.length"
      icon="i-tabler-alert-square-rounded"
      title="Nema dostupnih recenzija."
      description="Trenutno nema dostupnih recenzija za prikaz."
      :ui="{ body: 'max-w-full' }"
    />

    <div v-else class="flex flex-col gap-4">
      <UCard v-for="review in reviewsData.reviews" :key="review.id">
        <UUser
          :name="`@${review.reviewer.username}`"
          size="md"
          :avatar="{ src: review.reviewer.profile_image || '/static/default_profile_pic.png' }"
          :ui="{ name: 'text-lg font-semibold' }"
        />
        <Stars :stars="review.rating" />
        <p>{{ review.comment || 'Bez komentara' }}</p>
      </UCard>
    </div>
  </div>
</template>
