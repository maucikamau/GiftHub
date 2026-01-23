<script setup lang="ts">
import { ref } from 'vue'

interface FeedbackResult {
  rating: number
  comment: string
}

const { donorName } = defineProps<{
  donorId: number
  donorName: string
}>()

const emit = defineEmits<{
  (e: 'close', result: FeedbackResult | null): void
}>()

const rating = ref<number>(0)
const comment = ref('')
const hoveredRating = ref<number>(0)

function handleSubmit() {
  if (rating.value > 0) {
    emit('close', {
      rating: rating.value,
      comment: comment.value,
    })
  }
}

function handleSkip() {
  emit('close', null)
}

function setRating(value: number) {
  rating.value = value
}

function setHoveredRating(value: number) {
  hoveredRating.value = value
}

function clearHoveredRating() {
  hoveredRating.value = 0
}

function getRatingLabel(ratingValue: number): string {
  switch (ratingValue) {
    case 1: return 'Loše'
    case 2: return 'Ispodprosječno'
    case 3: return 'Prosječno'
    case 4: return 'Dobro'
    case 5: return 'Odlično'
    default: return ''
  }
}
</script>

<template>
  <UModal>
    <template #title>
      <div class="flex gap-3 items-center">
        <UIcon name="icon-park-solid:check-one" class="text-success-600 size-7" />
        <h3 class="text-md font-medium text-neutral-900">
          Hvala što ste potvrdili primopredaju!
        </h3>
      </div>
    </template>
    <template #body>
      <div class="space-y-6">
        <div class="flex items-start gap-3 p-4 -mx-3 bg-primary-50 rounded-lg">
          <div class="shrink-0">
            <UIcon name="i-lucide:star" class="text-primary-600 size-6" />
          </div>
          <div>
            <p class="text-neutral-900 font-medium">
              Želite li ostaviti recenziju za <strong>@{{ donorName }}</strong>?
            </p>
            <p class="text-sm text-neutral-600 mt-1">
              Vaša recenzija pomaže u izgradnji povjerenja u zajednici.
            </p>
          </div>
        </div>

        <div class="space-y-3">
          <UFormField label="Ocjena *">
            <div class="flex gap-4 my-2 items-center">
              <div class="flex gap-2">
                <button
                  v-for="star in 5"
                  :key="star"
                  type="button"
                  class="transition-transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-primary-500 rounded"
                  @click="setRating(star)"
                  @mouseenter="setHoveredRating(star)"
                  @mouseleave="clearHoveredRating"
                >
                  <UIcon
                    name="solar:star-bold-duotone"
                    class="size-10" :class="[
                      (hoveredRating >= star || (!hoveredRating && rating >= star))
                        ? 'text-yellow-400 fill-yellow-400'
                        : 'text-neutral-300',
                    ]"
                  />
                </button>
              </div>
              <p v-if="rating > 0" class="text-xl font-medium text-neutral-700">
                {{ getRatingLabel(rating) }}
              </p>
            </div>
          </UFormField>
        </div>

        <div class="space-y-2">
          <UFormField label="Komentar" help="Vaš komentar će biti vidljiv drugim korisnicima.">
            <UTextarea
              v-model="comment"
              placeholder="Podijelite svoje iskustvo..."
              :rows="4"
              class="w-full"
              :ui="{ base: 'resize-none' }"
            />
          </UFormField>
        </div>
      </div>
    </template>
    <template #footer>
      <UButton
        icon="i-lucide:send"
        label="Pošalji recenziju"
        color="primary"
        :disabled="rating === 0"
        @click="handleSubmit"
      />
      <UButton
        label="Ne želim ostaviti recenziju"
        color="neutral"
        variant="ghost"
        @click="handleSkip"
      />
    </template>
  </UModal>
</template>
