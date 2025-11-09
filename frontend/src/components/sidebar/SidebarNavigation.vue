<script setup lang="ts">
import { computed, onMounted, useTemplateRef, watch } from 'vue'
import { useRoute } from 'vue-router'
import { can } from '@/lib/permissions'

const { items } = defineProps<{
  items: Array<{
    name: string
    icon: string
    to: string
    permission?: string
  }>
}>()
const route = useRoute()
const indicatorRef = useTemplateRef('indicator')
const navContainer = useTemplateRef('navContainer')

const userItems = computed(() => {
  return items.filter((item) => {
    if (item.permission) {
      // Here you would check the user's permissions
      // For this example, we'll assume all permissions are granted
      return can(item.permission)
    }
    return true
  })
})

function updateIndicator() {
  if (!indicatorRef.value || !navContainer.value)
    return

  const activeItem = navContainer.value.querySelector<HTMLDivElement>('.indicator-active')
  if (activeItem) {
    indicatorRef.value.style.transform = `translateY(${activeItem.offsetTop + 8}px)`
    indicatorRef.value.style.height = `${activeItem.offsetHeight - 16}px`
  }
}

watch(route, updateIndicator, { flush: 'post' })

onMounted(updateIndicator)
</script>

<template>
  <div ref="navContainer" class="relative flex flex-col">
    <div ref="indicator" class="w-1 h-8 bg-primary absolute -left-4 transition-transform" />
    <UButton
      v-for="item in userItems"
      :key="item.name"
      :ui="{ base: 'px-2 py-2 text-base gap-2', leadingIcon: 'size-8' }"
      variant="ghost"
      active-color="primary"
      active-class="indicator-active"
      color="neutral"
      :icon="item.icon"
      :to="item.to"
    >
      {{ item.name }}
    </UButton>
  </div>
</template>

<style scoped>

</style>
