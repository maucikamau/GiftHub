<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useGetUserAvgReviews } from '@/services/reviews.ts'
import { useGetCities, useGetCurrentUser, useUpdateUserProfile } from '@/services/user.ts'
import { formatText } from '@/utils/formatting.ts'

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
const toast = useToast()

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
  if (!user.value || !form.value.location)
    return

  updateProfile({
    ...form.value,
    location_id: form.value.location,
    profile_image: profileImage.value,
  }, {
    onSuccess: () => {
      toast.add({
        color: 'success',
        title: 'Uspjeh',
        description: 'Profil je uspješno ažuriran.',
        duration: 3000,
      })
    },
  })
}

const isCitiesLoading = computed(() => !cities.value)

const average = ref(null)
const loading = ref(true)

watch(user, (val) => {
  if (!val)
    return

  fetch(`/api/reviews/stats/${val.id}`)
    .then(res => res.json())
    .then((data) => {
      average.value = data.average
      loading.value = false
    })
})

const { data: reviewData, isInitialLoading: fetchingAvg } = useGetUserAvgReviews(() => user.value?.id)
</script>

<template>
  <h1 class="font-medium text-4xl text-neutral-900">
    Pozdrav, {{ user?.first_name }}! 👋
  </h1>
  <div class="flex justify-between">
    <div class="max-w-2xl py-8">
      <h1 class="text-2xl font-semibold mb-6">
        Tvoj profil
      </h1>
      <div v-if="user" class="space-y-6">
        <div class="flex items-center gap-4">
          <UAvatar :src="profileImagePreview || '/static/default_profile_pic.png'" size="3xl" icon="i-lucide-user" />
          <div>
            <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange">
            <UButton
              color="neutral" variant="ghost" label="Promijeni sliku" icon="i-lucide-camera"
              @click="fileInput?.click()"
            />
          </div>
        </div>

        <UForm :state="form" class="flex flex-col w-md space-y-4" @submit="onSubmit">
          <UFormField label="Ime" name="first_name" orientation="horizontal">
            <UInput v-model="form.first_name" class="w-60" />
          </UFormField>

          <UFormField label="Prezime" name="last_name" orientation="horizontal">
            <UInput v-model="form.last_name" class="w-60" />
          </UFormField>

          <UFormField label="Korisničko ime" name="username" orientation="horizontal">
            <UInput v-model="form.username" class="w-60" />
          </UFormField>

          <template v-if="user.role === 'recipient_association'">
            <UFormField label="Naziv udruge" name="association_name" orientation="horizontal">
              <UInput v-model="form.association_name" class="w-60" />
            </UFormField>
            <UFormField label="Email udruge" name="association_email" orientation="horizontal">
              <UInput v-model="form.association_email" class="w-60" />
            </UFormField>
          </template>

          <UFormField label="Grad" name="location" orientation="horizontal">
            <div class="w-60">
              <USelectMenu
                v-model="form.location" :items="cities" label-key="cityName" value-key="id" searchable
                :loading="isCitiesLoading" class="w-full" placeholder="Odaberite grad"
              />
            </div>
          </UFormField>

          <div class="pt-4">
            <UButton type="submit" icon="i-lucide-save" :loading="isPending" label="Spremi promjene" />
          </div>
        </UForm>
      </div>
      <div v-else class="flex justify-center p-8">
        <UIcon name="i-lucide-loader-2" class="animate-spin text-4xl" />
      </div>
    </div>
    <div v-if="user?.role === 'donor'" class="mt-8 mr-4">
      <div v-if="fetchingAvg" class="flex">
        <USkeleton class="w-32 h-8" />
      </div>
      <div v-else-if="reviewData?.total === 0" class="text-sm text-neutral-600">
        Još nema recenzija!
      </div>
      <div v-else class="flex">
        <div class="text-2xl font-medium gap-2 flex items-end">
          <span class="text-6xl">{{ reviewData?.average || 0 }}</span>/5
        </div>
        <div class="flex flex-col ml-4">
          <Stars :stars="reviewData?.stars || 0" size="lg" />
          <UButton
            variant="ghost" trailing-icon="i-tabler:arrow-right" size="sm" class="mt-1"
            :to="{ name: 'recenzije', params: { userId: user?.id } }"
          >
            Pogledaj {{ formatText(reviewData?.total || 0, 'recenzij') }}
          </UButton>
        </div>
      </div>
    </div>
  </div>
</template>
