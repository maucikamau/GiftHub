<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { computed } from 'vue'
import Logo from '@/assets/PlayForward_Logo.svg'
import RegisterCardAssociation from '@/components/register/RegisterCardAssociation.vue'
import RegisterCardBasicInfo from '@/components/register/RegisterCardBasicInfo.vue'
import RegisterCardRecipient from '@/components/register/RegisterCardRecipient.vue'
import RegisterCardType from '@/components/register/RegisterCardType.vue'
import { OnboardingStep, useOnboardingStore } from '@/stores/onboarding.ts'
import { useUserStore } from '@/stores/user.ts'

const store = useOnboardingStore()
const userStore = useUserStore()
const { steps } = storeToRefs(store)
const { user } = storeToRefs(userStore)

interface StepDefinition {
  title: string
  component: any
}

const definitions: Record<OnboardingStep, StepDefinition> = {
  [OnboardingStep.USER_ROLE]: { title: 'Dobrodošao! Upoznajmo se.', component: RegisterCardType },
  [OnboardingStep.DONOR_BASIC_INFO]: {
    title: '🙌 Hvala ti - puno nam značiš!',
    component: RegisterCardBasicInfo,
  },
  [OnboardingStep.RECIPIENT_TYPE]: {
    title: 'Drago nam je što si ovdje.',
    component: RegisterCardRecipient,
  },
  [OnboardingStep.RECIPIENT_BASIC_INFO]: {
    title: 'Još samo malo i gotovo!',
    component: RegisterCardBasicInfo,
  },
  [OnboardingStep.ASSOCIATION_INFO]: {
    title: 'Trebamo informacije o udruzi 💕',
    component: RegisterCardAssociation,
  },
}

const activeStep = computed(() => definitions[steps.value[0]!])
</script>

<template>
  <div v-motion-fade-visible class="grid place-items-center w-full h-full">
    <div class="p-0.5 bg-brand-gradient rounded-xl shadow-lg w-2xl">
      <div class="p-8 bg-white rounded-xl">
        <img :src="Logo" class="h-18 mx-auto my-4">
        <br>
        <p class="font-medium text-2xl xl:text-3xl">
          {{ activeStep.title }}
        </p>
        <p class="mt-2 mb-16 font-medium text-xs xl:text-sm text-neutral-600">
          Prijavljen si kao: <span class="font-bold text-neutral-700">{{ user.email }}</span>
          <UButton variant="outline" to="/odjava" color="neutral" class="ml-4">
            Odjava
          </UButton>
        </p>
        <div class="my-4 relative overflow-hidden">
          <Transition :name="store.stepTransition" mode="out-in">
            <div :key="activeStep.component">
              <component :is="activeStep.component" />
            </div>
          </Transition>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.template-right-leave-active,
.template-right-enter-active,
.template-left-leave-active,
.template-left-enter-active {
  transition:
    transform 0.4s,
    opacity 0.4s;
  pointer-events: none;
  will-change: transform, opacity;
}

.template-right-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.template-right-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}

.template-left-enter-from {
  opacity: 0;
  transform: translateX(-100%);
}

.template-left-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
