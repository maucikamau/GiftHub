<script setup lang="ts">
import type { Component } from 'vue'
import { shallowRef, watch } from 'vue'
import { RouterView, useRoute } from 'vue-router'

const layout = shallowRef<Component | string>('div')
const layoutProps = shallowRef<Record<string, any>>({})

const route = useRoute()

watch(() => route.meta, (newMeta) => {
  layout.value = newMeta.layout as Component || 'div'
  layoutProps.value = newMeta.layoutProps || {}
}, { immediate: true })
</script>

<template>
  <UApp>
    <component :is="layout" v-bind="layoutProps">
      <RouterView />
    </component>
  </UApp>
</template>

<style scoped></style>
