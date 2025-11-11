import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { getMe, logout, registerAssociationInfo, registerBasicUserInfo } from '@/api/user.ts'
import { getCSRFToken } from '@/lib/django.ts'
import { permissionsProvider } from '@/lib/permissions.ts'

export const UserRoles = {
  donor: 'Donor',
  recipient: 'Primatelj',
  recipient_individual: 'Primatelj',
  recipient_association: 'Udruga',
}

export function useGetCurrentUser() {
  return useQuery({
    queryKey: ['users', 'me'],
    queryFn: async () => {
      const user = await getMe()

      if (user?.permissions)
        permissionsProvider.update(user.permissions)

      sessionStorage.removeItem('csrftoken')
      await getCSRFToken()

      return user
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useLogout() {
  const qc = useQueryClient()

  return useMutation({
    mutationFn: logout,
    async onSuccess() {
      await qc.invalidateQueries({ queryKey: ['users', 'me'] })
    },
  })
}

export function useRegisterBasicUserInfo() {
  const qc = useQueryClient()

  return useMutation({
    mutationFn: registerBasicUserInfo,
    async onSuccess() {
      await qc.invalidateQueries({ queryKey: ['users', 'me'] })
    },
  })
}

export function useRegisterAssociationInfo() {
  const qc = useQueryClient()

  return useMutation({
    mutationFn: registerAssociationInfo,
    async onSuccess() {
      await qc.invalidateQueries({ queryKey: ['users', 'me'] })
    },
  })
}
