import { getMe } from '@/api/user.ts'
import { permissionsProvider } from '@/lib/permissions.ts'
import { qc } from '@/lib/vueQuery.ts'
import router from './index.ts'

router.beforeEach(async (to, from, next) => {
  // check if user is authenticated
  const currentUser = await qc.fetchQuery({
    queryKey: ['users', 'me'],
    queryFn: getMe,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: false,
  }).catch(() => null)

  if (to.meta.public)
    return next()

  if (!currentUser) {
    // redirect to login page
    if (to.name === 'prijava')
      return next()

    return next({ name: 'prijava', query: to.name !== 'odjava' ? { next: to.fullPath } : {} })
  }

  if (currentUser.permissions)
    permissionsProvider.update(currentUser.permissions)

  const userFinishedOnboarding = currentUser.registration_step === 3

  if (to.name === 'odjava')
    return next()

  if (!userFinishedOnboarding && to.name !== 'onboarding') {
    return next({ name: 'onboarding' })
  }
  else if (userFinishedOnboarding && to.name === 'onboarding') {
    return next({ name: 'home' })
  }

  if (to.name === 'prijava')
    return next({ name: 'home' })

  next()
})
