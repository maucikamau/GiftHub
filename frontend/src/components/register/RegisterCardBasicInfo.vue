<script setup lang="ts">
import type { UserBasicInfo } from '@/types/user.ts'
import { storeToRefs } from 'pinia'
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { userBasicInfoSchema } from '@/schemas/user.ts'
import { useGetCurrentUser, useRegisterBasicUserInfo } from '@/services/user.ts'
import { useOnboardingStore } from '@/stores/onboarding.ts'

const store = useOnboardingStore()
const { data: user, refetch: refetchUser } = useGetCurrentUser()
const router = useRouter()
const { submitEnabled } = storeToRefs(store)

const cities = ref([
  { label: 'Zagreb', value: 'Zagreb' },
  { label: 'Split', value: 'Split' },
  { label: 'Rijeka', value: 'Rijeka' },
  { label: 'Osijek', value: 'Osijek' },
  { label: 'Zadar', value: 'Zadar' },
])

const basicInfo = ref<Partial<UserBasicInfo>>({
  first_name: user.value?.first_name || '',
  last_name: user.value?.last_name || '',
  username: user.value?.username || '',
  location: user.value?.location || '',
  termsAccepted: false,
})

watch(
  basicInfo,
  () => {
    // validate against zod schema
    const result = userBasicInfoSchema.safeParse(basicInfo.value)
    submitEnabled.value = result.success
  },
  { deep: true, immediate: true },
)

const { mutateAsync: saveUserInfo } = useRegisterBasicUserInfo()

async function onSubmit() {
  if (!submitEnabled.value || !user.value)
    return

  await saveUserInfo(basicInfo.value as UserBasicInfo, {
    onError(error) {
      console.error('Error saving user basic info:', error)
    },
  })

  // const newUser = await refetchUser()

  if (user.value.role === 'recipient_association') {
    store.nextStep()
  }
  else {
    console.log('Registration complete, redirecting to home page.')

    await router.push({ name: 'home' })
  }
}
</script>

<template>
  <UForm v-if="user" :schema="userBasicInfoSchema" :state="basicInfo" class="grid grid-cols-2 gap-4 mb-4" @submit="onSubmit">
    <div class="flex justify-start flex-col">
      <p class="m-1 font-semibold">
        Ime
      </p>
      <UInput v-model="basicInfo.first_name" placeholder="Unesite ime" />
    </div>
    <div class="flex flex-col">
      <p class="m-1 font-semibold">
        Prezime
      </p>
      <UInput v-model="basicInfo.last_name" placeholder="Unesite prezime" />
    </div>
    <div class="flex flex-col">
      <p class="m-1 font-semibold">
        Korisničko ime
      </p>
      <UInput v-model="basicInfo.username" placeholder="Unesite korisničko ime" />
      <p class="m-1 text-xs">
        Tvoje korisničko ime je <span class="font-semibold">javno</span> i bit će korišteno za
        komunikaciju sa drugima u chatu.
      </p>
    </div>
    <div class="flex flex-col">
      <p class="m-1 font-semibold">
        Mjesto
      </p>
      <USelectMenu
        v-model="basicInfo.location" value-key="value" :items="cities"
        placeholder="Odaberite mjesto"
      />
      <p class="m-1 text-xs">
        Koristimo mjesto za lakši pronalazak oglasa u tvom mjestu.
        Uvijek možeš promijeniti mjesto za pojedinačne oglase.
      </p>
    </div>

    <div class="flex items-center col-span-2 my-4">
      <UCheckbox
        v-model="basicInfo.termsAccepted"
        size="lg"
        label="Potvrđujem da sam punoljetna osoba i slažem se s Uvjetima korištenja."
      />
    </div>

    <div class="h-10 col-span-2 justify-between flex mt-16">
      <UButton
        variant="ghost"
        color="neutral"
        size="xl"
        @click="store.previousStep"
      >
        <p>← Natrag</p>
      </UButton>
      <UButton
        v-if="user.role === 'recipient_association'"
        :disabled="!store.submitEnabled"
        :variant="store.submitEnabled ? 'solid' : 'ghost'"
        color="neutral"
        size="xl"
        type="submit"
      >
        <p>Nastavak ➜</p>
      </UButton>
      <UButton
        v-else
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
