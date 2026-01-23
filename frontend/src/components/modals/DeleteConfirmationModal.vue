<script setup lang="ts">
interface Props {
  itemName: string
  itemType: 'listing' | 'campaign'
}

defineProps<Props>()

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
  <UModal title="Potvrda brisanja">
    <template #body>
      <div class="space-y-4">
        <div class="flex gap-3 p-4 bg-error-50 rounded-lg">
          <div class="shrink-0">
            <UIcon name="i-lucide:alert-triangle" class="text-error-600 size-8" />
          </div>
          <div>
            <p class="text-neutral-900 font-semibold mb-1">
              Jeste li sigurni da želite obrisati {{ itemType === 'listing' ? 'oglas' : 'kampanju' }}?
            </p>
            <p class="text-red-600 font-medium text-sm break-all">
              {{ itemName }}
            </p>
            <p class="text-neutral-600 text-sm mt-3">
              Ova radnja se ne može poništiti.
            </p>
          </div>
        </div>
      </div>
    </template>
    <template #footer>
      <UButton
        icon="i-lucide:trash-2"
        label="Obriši"
        color="error"
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
