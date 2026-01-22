<script setup lang="ts">
const emit = defineEmits<{
  (e: 'close', confirmed: boolean): void
}>()

function handleConfirm() {
  emit('close', true)
}

function handleCancel() {
  emit('close', false)
}
</script>

<template>
  <UModal title="Potvrda primopredaje">
    <template #body>
      <div class="space-y-4">
        <div class="flex items-center gap-3 p-4 bg-success-50 rounded-lg">
          <div class="shrink-0">
            <UIcon name="i-lucide:package-check" class="text-success-600 size-8" />
          </div>
          <div>
            <p class="text-neutral-900 font-medium">
              Ovime potvrđujete da ste preuzeli donaciju.
            </p>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <UButton
        icon="i-lucide:check"
        label="Potvrdi primopredaju"
        color="success"
        @click="handleConfirm"
      />
      <UButton
        label="Odustani"
        color="neutral"
        variant="ghost"
        @click="handleCancel"
      />
    </template>
  </UModal>
</template>
