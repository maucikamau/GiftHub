<script setup lang="ts">
import type { UserAssociationInfo } from '@/types/user.ts'
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { associationSchema } from '@/schemas/user.ts'
import { useRegisterAssociationInfo } from '@/services/user'
import { useOnboardingStore } from '@/stores/onboarding.ts'

const store = useOnboardingStore()
const router = useRouter()

const associationState = ref<Partial<UserAssociationInfo>>({
  association_name: undefined,
  association_email: undefined,
})

const { mutateAsync: saveAssociationInfo } = useRegisterAssociationInfo()

async function handleSubmit() {
  const payload = associationSchema.safeParse(associationState.value)
  if (!payload.success)
    return

  await saveAssociationInfo(payload.data)

  await router.push('/')
}

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
  <UForm :state="associationState" :schema="associationSchema" class="flex flex-col gap-4" @click="handleSubmit">
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
    <div class="flex justify-end mt-16">
      <UButton
        :disabled="!store.submitEnabled"
        :variant="store.submitEnabled ? 'solid' : 'outline'"
        color="success"
        size="xl"
        type="submit"
      >
        <p>Registriraj</p>
      </UButton>
    </div>
  </UForm>
</template>
