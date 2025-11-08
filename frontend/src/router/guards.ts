import { useUserStore } from '@/stores/user.ts'
import router from './index.ts'

router.beforeEach(async (to, from, next) => {
  // check if user is authenticated
  const userStore = useUserStore()

  if (to.meta.public)
    return next()

  const currentUser = await userStore.getCurrentUser().catch(() => undefined)

  const userFinishedOnboarding = currentUser && currentUser.registration_step === 3

  if (!currentUser) {
    // redirect to login page
    if (to.name === 'prijava')
      return next()

    return next({ name: 'prijava', query: to.name !== 'odjava' ? { next: to.fullPath } : {} })
  }

  if (to.name === 'odjava')
    return next()

  if (!userFinishedOnboarding && to.name !== 'onboarding') {
    return next({ name: 'onboarding' })
  }

  next()
})
