import { qc } from '@/lib/vueQuery.ts'
import { currentUserQuery } from '@/services/user.ts'
import router from './index.ts'

router.beforeEach(async (to, _from, next) => {
  if (to.meta.public || to.name === 'NotFound')
    return next()

  // check if user is authenticated
  const currentUser = await qc.fetchQuery(currentUserQuery).catch(() => null)

  if (!currentUser) {
    // redirect to login page
    if (to.meta.unauthenticatedOnly)
      return next()

    return next({ name: 'prijava', query: to.name !== 'odjava' ? { next: to.fullPath } : {} })
  }

  const userFinishedOnboarding = currentUser.registration_step === 3

  if (to.name === 'odjava')
    return next()

  if (!userFinishedOnboarding && to.name !== 'onboarding') {
    return next({ name: 'onboarding' })
  }

  if (to.name && to.name in ['onboarding', 'prijava']) {
    return next({ name: 'home' })
  }

  next()
})
