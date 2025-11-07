import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export enum UserRole {
  DONOR = 'donor',
  PRIMATELJ = 'primatelj',
  PRIMATELJ_PRIVATNA_OSOBA = 'primatelj-privatna-osoba',
  PRIMATELJ_UDRUGA = 'primatelj-udruga',
}

export enum OnboardingStep {
  USER_ROLE = 'user-role',
  DONOR_BASIC_INFO = 'donor-basic-info',
  RECIPIENT_TYPE = 'recipient-type',
  RECIPIENT_BASIC_INFO = 'primatelj-basic-info',
  ASSOCIATION_INFO = 'association-info',
}

export const useOnboardingStore = defineStore('onboarding', () => {
  const userRole = ref<UserRole | null>(null)

  const steps = ref<OnboardingStep[]>([OnboardingStep.USER_ROLE])
  const stepHistory = ref<OnboardingStep[]>([])

  const stepTransition = ref('template-right')

  function nextStep(...nextSteps: OnboardingStep[]) {
    steps.value.push(...nextSteps)
    stepHistory.value.push(steps.value.shift()!)
    stepTransition.value = 'template-right'
  }

  function previousStep() {
    const previousStep = stepHistory.value.pop()
    if (previousStep) {
      steps.value = [previousStep]
      stepTransition.value = 'template-left'
    }
  }

  const hasPreviousStep = computed(() => stepHistory.value.length > 0)

  function chooseRole(role: UserRole) {
    userRole.value = role
    if (role === UserRole.DONOR) {
      nextStep(OnboardingStep.DONOR_BASIC_INFO)
    }
    else if (role === UserRole.PRIMATELJ) {
      nextStep(OnboardingStep.RECIPIENT_TYPE)
    }
    else if (role === UserRole.PRIMATELJ_PRIVATNA_OSOBA) {
      nextStep(OnboardingStep.RECIPIENT_BASIC_INFO)
    }
    else if (role === UserRole.PRIMATELJ_UDRUGA) {
      nextStep(OnboardingStep.RECIPIENT_BASIC_INFO, OnboardingStep.ASSOCIATION_INFO)
    }
  }

  return {
    userRole,
    chooseRole,
    steps,
    nextStep,
    stepTransition,
    stepHistory,
    previousStep,
    hasPreviousStep,
  }
})
