import { useQueryClient } from '@tanstack/vue-query'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { registerUserRole } from '@/api/user.ts'
import { useGetCurrentUser } from '@/services/user.ts'

export enum UserRole {
  DONOR = 'donor',
  RECIPIENT = 'recipient',
  RECIPIENT_INDIVIDUAL = 'recipient_individual',
  RECIPIENT_ASSOCIATION = 'recipient_association',
}

export enum OnboardingStep {
  USER_ROLE = 'user-role',
  DONOR_BASIC_INFO = 'donor-basic-info',
  RECIPIENT_TYPE = 'recipient-type',
  RECIPIENT_BASIC_INFO = 'primatelj-basic-info',
  ASSOCIATION_INFO = 'association-info',
}

export const useOnboardingStore = defineStore('onboarding', () => {
  const { data: user } = useGetCurrentUser()
  const qc = useQueryClient()

  function getInitialSteps() {
    if (!user.value) {
      return [OnboardingStep.USER_ROLE]
    }

    const userOnStep = user.value?.registration_step

    if (user.value.role === 'donor') {
      return [OnboardingStep.DONOR_BASIC_INFO]
    }
    else if (userOnStep === 1) {
      return [OnboardingStep.RECIPIENT_TYPE]
    }
    else if (user.value.role === 'recipient_individual') {
      return [OnboardingStep.RECIPIENT_BASIC_INFO]
    }
    else if (user.value.role === 'recipient_association') {
      if (userOnStep === 2) {
        return [OnboardingStep.RECIPIENT_BASIC_INFO, OnboardingStep.ASSOCIATION_INFO]
      }
      else {
        return [OnboardingStep.ASSOCIATION_INFO]
      }
    }

    return [OnboardingStep.USER_ROLE]
  }

  const steps = ref<OnboardingStep[]>(getInitialSteps())
  const stepHistory = ref<OnboardingStep[]>([])
  const submitEnabled = ref(false)

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
  const hasNextStep = computed(() => steps.value.length > 1)

  async function chooseRole(role: UserRole) {
    // make an api request to set the user role
    if (role === UserRole.RECIPIENT) {
      nextStep(OnboardingStep.RECIPIENT_TYPE)
      return
    }

    const res = await registerUserRole(role).catch((error) => {
      console.error('Error registering user role:', error)
      // make ui feedback and don't continue
      return null
    })
    if (!res) {
      return
    }

    await qc.invalidateQueries({ queryKey: ['users', 'me'] })

    if (role === UserRole.DONOR) {
      nextStep(OnboardingStep.DONOR_BASIC_INFO)
    }
    else if (role === UserRole.RECIPIENT_INDIVIDUAL) {
      nextStep(OnboardingStep.RECIPIENT_BASIC_INFO)
    }
    else if (role === UserRole.RECIPIENT_ASSOCIATION) {
      nextStep(OnboardingStep.RECIPIENT_BASIC_INFO, OnboardingStep.ASSOCIATION_INFO)
    }
  }

  return {
    chooseRole,
    steps,
    nextStep,
    hasNextStep,
    submitEnabled,
    stepTransition,
    stepHistory,
    previousStep,
    hasPreviousStep,
  }
})
