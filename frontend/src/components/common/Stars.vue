<script setup lang="ts">
enum Sizes {
  sm = 'size-4',
  md = 'size-5',
  lg = 'size-7',
  xl = 'size-10',
}
const { size = 'md' } = defineProps<{ stars: number, size?: keyof typeof Sizes }>()
</script>

<template>
  <div class="flex items-center gap-1 my-1">
    <template v-for="n in (stars || 0)" :key="n">
      <UIcon name="solar:star-bold-duotone" class="text-yellow-400" :class="Sizes[size]" />
    </template>
    <template v-for="n in 5 - (stars || 0)" :key="n">
      <UIcon name="solar:star-bold-duotone" class="text-neutral-600" :class="Sizes[size]" />
    </template>
  </div>
</template>
