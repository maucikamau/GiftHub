<script setup lang="ts">
import { computed, ref } from 'vue'

interface Props {
  src: string | null | undefined
  alt?: string
  fallbackIcon?: string
  fallbackText?: string
  class?: string
  imgClass?: string
  aspectRatio?: string
  objectFit?: 'cover' | 'contain' | 'fill' | 'none' | 'scale-down'
}

const props = withDefaults(defineProps<Props>(), {
  alt: '',
  fallbackIcon: 'i-lucide:image-off',
  fallbackText: 'Slika nije dostupna',
  class: '',
  imgClass: '',
  aspectRatio: '16/9',
  objectFit: 'cover',
})

const isLoading = ref(true)
const hasError = ref(false)

const containerClasses = computed(() => props.class)

const imageClasses = computed(() => {
  const baseClasses = 'w-full h-full transition-opacity duration-300'
  const fitClass = `object-${props.objectFit}`
  const opacityClass = isLoading.value ? 'opacity-0' : 'opacity-100'
  return `${baseClasses} ${fitClass} ${opacityClass} ${props.imgClass}`
})

const aspectStyle = computed(() => ({
  aspectRatio: props.aspectRatio,
}))

function handleLoad() {
  isLoading.value = false
  hasError.value = false
}

function handleError() {
  isLoading.value = false
  hasError.value = true
}

const shouldShowFallback = computed(() => !props.src || hasError.value)
</script>

<template>
  <div :class="containerClasses" :style="aspectStyle" class="relative overflow-hidden rounded-lg bg-neutral-100">
    <!-- Loading skeleton -->
    <div
      v-if="isLoading && !shouldShowFallback"
      class="absolute inset-0 animate-pulse bg-gradient-to-r from-neutral-100 via-neutral-200 to-neutral-100 bg-[length:200%_100%]"
      style="animation: shimmer 1.5s infinite"
    />

    <!-- Fallback state -->
    <div
      v-if="shouldShowFallback"
      class="absolute inset-0 flex flex-col items-center justify-center gap-2 bg-neutral-50 text-neutral-400"
    >
      <UIcon :name="fallbackIcon" class="size-12" />
      <span class="text-sm font-medium">{{ fallbackText }}</span>
    </div>

    <!-- Actual image -->
    <img
      v-if="!shouldShowFallback"
      :src="src!"
      :alt="alt"
      :class="imageClasses"
      @load="handleLoad"
      @error="handleError"
    >
  </div>
</template>

<style scoped>
@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
