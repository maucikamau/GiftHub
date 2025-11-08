import type { User, UserBasicInfo } from '@/types/user.ts'
import { api } from '@/lib/apiClient.ts'

export async function getMe() {
  return await api<User | undefined>('users/me/').json()
}

export async function logout() {
  return await api('users/logout/').json()
}

export async function registerUserType(role: User['role']) {
  return await api('users/register/type/', {
    method: 'PATCH',
    json: { role },
  }).json()
}

export async function registerBasicUserInfo(userInfo: UserBasicInfo) {
  return await api<UserBasicInfo>('users/register/basicinfo/', {
    method: 'PATCH',
    json: { ...userInfo },
  }).json()
}
