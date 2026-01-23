<script setup lang="ts">
import type { FormError } from '@nuxt/ui/runtime/types'
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { signupWithEmail } from '@/api/auth.ts'
import Logo from '@/assets/PlayForward_Logo.svg'

type Optional<T> = T | undefined

const state = reactive<{
  email: Optional<string>
  password: Optional<string>
  error: Optional<string>
}>({
  email: undefined,
  password: undefined,
  error: undefined,
})

const router = useRouter()

type Schema = typeof state

const emailRegex = /^[^\s@]+@[^\s@][^\s.@]*\.[^\s@]+$/

function validate(state: Partial<Schema>): FormError[] {
  const errors = []
  if (!state.email)
    errors.push({ name: 'email', message: 'Morate unijeti e-mail.' })
  if (!state.password)
    errors.push({ name: 'password', message: 'Morate unijeti lozinku.' })

  if (state.email && !emailRegex.test(state.email))
    errors.push({ name: 'email', message: 'E-mail nije valjan' })

  return errors
}

function registerWrapper() {
  state.error = undefined
  return signupWithEmail(state.email, state.password)
    .then(() => router.push('/'))
    .catch((err: any) => {
      console.log(err.detail)
      state.error = err.detail.map(e => e.message) || [err.message] || ['Nepoznata pogreška. Pokušajte ponovno.']
    })
}
</script>

<template>
  <div v-motion-fade-visible class="grid place-items-center w-full h-full">
    <div class="p-0.5 bg-brand-gradient rounded-xl shadow-lg w-2xl">
      <div class="p-8 bg-white rounded-xl">
        <img :src="Logo" class="h-18 mx-auto my-4">
        <br>
        <p class="font-medium text-2xl xl:text-3xl">
          Stvorimo tvoj novi račun 🥰
        </p>
        <p class="mt-2 mb-16 font-medium text-xs xl:text-sm text-neutral-600">
          Već imaš račun?
          <UButton variant="outline" to="/prijava" color="neutral" class="ml-4">
            Prijava
          </UButton>
        </p>
        <div class="my-4 relative overflow-hidden">
          <UForm
            :validate="validate"
            :state="state"
            class="mb-4 flex flex-col gap-4"
            @submit="registerWrapper"
          >
            <UFormField label="E-mail" name="email" required>
              <UInput
                v-model="state.email"
                class="w-full"
                size="lg"
                placeholder="ime.prezime@example.org"
              />
            </UFormField>
            <UFormField label="Lozinka" name="password" required>
              <UInput
                v-model="state.password"
                class="w-full"
                size="lg"
                type="password"
                placeholder="Lozinka"
              />
            </UFormField>
            <UButton type="submit" color="secondary" size="xl" label="Stvori novi račun" block />
            <div v-if="state.error?.length > 0" class="flex flex-col gap-1">
              <p class="text-red-600 font-semibold">
                Neuspješna registracija.
              </p>
              <div v-for="err in state.error || []" :key="err" class="text-red-500 items-center flex gap-3">
                <UIcon name="i-material-symbols:error-outline" />
                <span>{{ err }}</span>
              </div>
            </div>
          </UForm>
        </div>
      </div>
    </div>
  </div>
</template>
