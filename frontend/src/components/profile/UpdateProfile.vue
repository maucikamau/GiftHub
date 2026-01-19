<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useGetCurrentUser, useGetCities, useUpdateUserProfile } from '@/services/user.ts'

const { data: user } = useGetCurrentUser()
const { data: cities } = useGetCities()
const { mutate: updateProfile, isPending } = useUpdateUserProfile()

const form = ref({
  first_name: '',
  last_name: '',
  username: '',
  location: undefined as number | undefined,
  association_name: '',
  association_email: '',
})

const fileInput = ref<HTMLInputElement | null>(null)
const profileImage = ref<File | undefined>(undefined)
const profileImagePreview = ref<string | undefined>(undefined)

watch(user, (newUser) => {
  if (newUser) {
    form.value = {
      first_name: newUser.first_name,
      last_name: newUser.last_name,
      username: newUser.username,
      location: newUser.location?.id,
      association_name: 'association_name' in newUser ? newUser.association_name : '',
      association_email: 'association_email' in newUser ? newUser.association_email : '',
    }
    if (newUser.profile_image) {
      profileImagePreview.value = newUser.profile_image
    }
  }
}, { immediate: true })

function onFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    profileImage.value = target.files[0]
    profileImagePreview.value = URL.createObjectURL(target.files[0])
  }
}

function onSubmit() {
  if (!user.value || !form.value.location) return

  updateProfile({
    ...form.value,
    location_id: form.value.location,
    profile_image: profileImage.value,
  })
}

const isCitiesLoading = computed(() => !cities.value)
</script>

<template>
  <h1 class="font-medium text-4xl text-neutral-900">
    Pozdrav, {{ user.first_name }}! 👋
  </h1>
  <div class="flex justify-between">
    <div class="max-w-2xl py-8 px-4">
      <h1 class="text-2xl font-bold mb-6">Uredi Profil</h1>
      <div v-if="user" class="space-y-6">
        <div class="flex items-center gap-4">
          <UAvatar :src="profileImagePreview || '/static/default_profile_pic.png'" size="3xl" icon="i-lucide-user" />
          <div>
            <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange">
            <UButton color="white" label="Promijeni sliku" icon="i-lucide-camera" @click="fileInput?.click()" />
          </div>
        </div>

        <UForm :state="form" @submit="onSubmit" class="flex flex-col space-y-4">
          <UFormGroup label="Ime" name="first_name" class="flex flex-row items-center gap-2">
            <p>Ime: </p>
            <UInput v-model="form.first_name" />
          </UFormGroup>

          <UFormGroup label="Prezime" name="last_name" class="flex flex-row items-center gap-2">
            <p>Prezime: </p>
            <UInput v-model="form.last_name" />
          </UFormGroup>

          <UFormGroup label="Korisničko ime" name="username" class="flex flex-row items-center gap-2">
            <p>Korisničko ime: </p>
            <UInput v-model="form.username" />
          </UFormGroup>

          <template v-if="user.role === 'recipient_association'">
            <UFormGroup label="Naziv udruge" name="association_name" class="flex flex-row items-center gap-2">
              <p>Naziv udruge: </p>
              <UInput v-model="form.association_name" />
            </UFormGroup>
            <UFormGroup label="Email udruge" name="association_email" class="flex flex-row items-center gap-2">
              <p>Email udruge: </p>
              <UInput v-model="form.association_email" />
            </UFormGroup>
          </template>

          <UFormGroup label="Grad" name="location" class="flex flex-row items-center gap-2">
            <p>Grad: </p>
            <USelectMenu v-model="form.location" :items="cities" label-key="cityName" value-key="id" searchable
              :loading="isCitiesLoading" placeholder="Odaberite grad" />
          </UFormGroup>

          <div class="pt-4">
            <UButton type="submit" :loading="isPending" label="Spremi promjene" />
          </div>
        </UForm>
      </div>
      <div v-else class="flex justify-center p-8">
        <UIcon name="i-lucide-loader-2" class="animate-spin text-4xl" />
      </div>
    </div>
    <div class="mt-8 mr-4">
      <div class="text-2xl font-medium gap-2 flex items-end">
        <span class="text-6xl">4.5</span>/5
      </div>
      <div class="flex flex-col ml-4">
        <div class="flex items-center gap-1 ml-2">
          <UIcon name="solar:star-bold-duotone" class="size-7 text-yellow-400" />
          <UIcon name="solar:star-bold-duotone" class="size-7 text-yellow-400" />
          <UIcon name="solar:star-bold-duotone" class="size-7 text-yellow-400" />
          <UIcon name="solar:star-bold-duotone" class="size-7 text-yellow-400" />
          <UIcon name="solar:star-bold-duotone" class="size-7 text-neutral-600" />
        </div>
        <UButton variant="ghost" trailing-icon="i-tabler:arrow-right" size="sm" class="mt-1">
          Pogledaj recenzije
        </UButton>
      </div>
    </div>
  </div>
</template>
