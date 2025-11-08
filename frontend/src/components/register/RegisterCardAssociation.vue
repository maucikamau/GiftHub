<script setup lang="ts">
import type { AssociationSchemaState } from '@/types/user.ts'
import { ref, watch } from 'vue'
import { associationSchema } from '@/schemas/user.ts'
import { useOnboardingStore } from '@/stores/onboarding.ts'

const store = useOnboardingStore()

const associationState = ref<Partial<AssociationSchemaState>>({
  association_name: undefined,
  association_email: undefined,
})

watch(
  associationState,
  () => {
    // validate with zod
    const result = associationSchema.safeParse(associationState.value)
    store.submitEnabled = result.success
  },
  { deep: true, immediate: true },
)
</script>

<template>
  <UForm :state="associationState" :schema="associationSchema" class="flex flex-col gap-4">
    <UFormField label="Ime udruge">
      <UInput
        v-model="associationState.association_name"
        placeholder="Unesite ime udruge"
        size="lg"
        :ui="{ trailing: 'pe-1' }"
        class="w-full"
      />
    </UFormField>
    <UFormField
      label="Email udruge"
    >
      <template #help>
        <p>
          S mailom potvrđujemo da ste jedini ovlašteni vlasnik računa za udrugu.
          U slučaju pokušaja prijevare i sličnog, ovaj ćemo mail koristiti za <b>kontakt</b>.
        </p>
      </template>
      <UInput
        v-model="associationState.association_email"
        placeholder="Unesite email udruge"
        :ui="{ trailing: 'pe-1' }"
        size="lg"
        class="w-full"
      />
    </UFormField>
    <div class="flex justify-between mt-16">
      <UButton
        variant="ghost"
        color="neutral"
        size="xl"
        @click="store.previousStep"
      >
        <p>← Natrag</p>
      </UButton>
      <UButton
        :disabled="!store.submitEnabled"
        :variant="store.submitEnabled ? 'solid' : 'outline'"
        color="success"
        size="xl"
        @click="store.register"
      >
        <p>Registriraj</p>
      </UButton>
    </div>
  </UForm>
</template>
