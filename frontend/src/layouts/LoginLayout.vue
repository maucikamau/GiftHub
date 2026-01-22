<script setup lang="ts">
import type { FormError } from '@nuxt/ui/runtime/types'
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { loginWithEmail, loginWithOauth } from '@/api/auth.ts'
import Logo from '@/assets/PlayForward_Logo.svg'
import { OAuthProviders } from '@/types/auth.ts'

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

function loginWithPasswordWrapper() {
  state.error = undefined
  return loginWithEmail(state.email, state.password).catch((err: any) => {
    state.error = err.message || 'Neuspjesna prijava. Pokusajte ponovno.'
  }).then(() => {
    router.push('/')
  })
}
</script>

<template>
  <div
    class="min-h-screen bg-[url(/static/PlayForward_Banner.png)] bg-center bg-no-repeat bg-cover flex flex-col"
  >
    <div class="m-4 layout gap-4 flex-1">
      <div
        class="[grid-area:hello] bg-brand-gradient-softer flex flex-col justify-center items-center p-4 rounded-xl"
      >
        <p class="block font-bold text-2xl lg:text-4xl lg:mb-4 text-surface-800">
          Zašto bi stare igračke skupljale prašinu?
        </p>
        <p class=" block text-lg lg:text-xl text-[#968F70]">
          Podijeli svoje stare igračke i pomozi zajednici.
        </p>
      </div>
      <div class="grid [grid-area:login] place-items-center w-full h-full">
        <div
          class="p-[3px] bg-linear-to-r h-full max-w-[660px] w-full max-h-[720px] from-[#f9b233] to-[#ef4fa6] rounded-2xl"
        >
          <div class="bg-white rounded-2xl h-full py-6 px-4 grid place-items-center">
            <div class="flex flex-col w-full px-12">
              <img :src="Logo" class="text-6xl h-16 w-min">
              <UForm
                :validate="validate"
                :state="state"
                class="my-4 flex flex-col gap-4"
                @submit="loginWithPasswordWrapper"
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
                <UButton type="submit" size="xl" label="Prijava" icon="i-lucide:log-in" block />
                <p v-if="state.error" class="text-red-500 text-xs">
                  {{ state.error }}
                </p>
                <p class="mt-2 font-medium text-xs xl:text-sm text-neutral-600 flex items-center">
                  Još nemaš račun?
                  <UButton variant="outline" icon="i-ri:user-add-line" to="/registracija" color="neutral" class="ml-4">
                    Registriraj se
                  </UButton>
                </p>
              </UForm>
              <USeparator label="ili" />
              <UButton
                variant="outline" color="neutral" block size="xl" class="my-2"
                icon="i-logos:google-icon" @click="loginWithOauth(OAuthProviders.GOOGLE)"
              >
                Prijava s Google računom
              </UButton>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.layout {
  display: grid;
  grid-template-areas: 'hello login login login';
}

@media only screen and (max-width: 1100px) {
  .layout {
    display: grid;
    grid-template-areas:
    'hello'
    'login';
  }
}
</style>
