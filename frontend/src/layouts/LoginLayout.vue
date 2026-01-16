<script setup lang="ts">
import type { FormError } from '@nuxt/ui/runtime/types'
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { loginWithOauth, loginWithPassword } from '@/api/auth.ts'
import Logo from '@/assets/PlayForward_Logo.svg'
import { OAuthProviders } from '@/types/auth.ts'

const state = reactive({
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
    errors.push({ name: 'email', message: 'Required' })
  if (!state.password)
    errors.push({ name: 'password', message: 'Required' })

  if (state.email && !emailRegex.test(state.email))
    errors.push({ name: 'email', message: 'Invalid email' })

  return errors
}

function loginWithPasswordWrapper() {
  state.error = undefined
  return loginWithPassword(state.email, state.password).catch((err: any) => {
    state.error = err.message || 'Login failed'
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
        <p class="block font-bold text-2xl lg:text-4xl lg:mb-4 text-[#69644F]">
          Zašto bi stare igračke skupljale prašinu?
        </p>
        <p class=" block text-lg lg:text-xl text-[#968F70]">
          Podijeli svoje stare igračke i pomozi zajednici.
        </p>
      </div>
      <div class="grid [grid-area:login] place-items-center w-full h-full">
        <div
          class="p-[3px] bg-gradient-to-r h-full max-w-[660px] w-full max-h-[720px] from-[#f9b233] to-[#ef4fa6] rounded-2xl"
        >
          <div class="bg-white rounded-2xl h-full py-6 px-4 grid place-items-center">
            <div class="flex flex-col">
              <img :src="Logo" class="text-6xl h-16 w-min">
              <p class="font-medium text-lg pr-8 py-4">
                Da biste pristupili platformi, morate se prijaviti.
              </p>
              <UForm
                :validate="validate"
                :state="state"
                class="mb-4 flex flex-col gap-4"
                @submit="loginWithPasswordWrapper"
              >
                <UFormField label="Email" name="email" required>
                  <UInput
                    v-model="state.email"
                    class="w-full"
                    size="lg"
                    placeholder="Enter your email"
                  />
                </UFormField>
                <UFormField label="Password" name="password" required>
                  <UInput
                    v-model="state.password"
                    class="w-full"
                    size="lg"
                    type="password"
                    placeholder="Password"
                  />
                </UFormField>
                <UButton type="submit" size="lg" label="Prijava" icon="i-lucide:log-in" block />
                <p v-if="state.error" class="text-red-500">
                  {{ state.error }}
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
