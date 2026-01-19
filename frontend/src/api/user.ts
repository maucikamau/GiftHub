import type { LocationCity, User, UserAssociationInfo, UserBasicInfo } from '@/types/user.ts'
import { api } from '@/lib/apiClient.ts'

export async function getMe() {
  return await api<User | undefined>('users/me/').json()
}

export async function logout() {
  // invalidate csrf token, it changes on user login/logout
  sessionStorage.removeItem('csrftoken')
  return await api('users/logout/').json()
}

export async function getCities() {
  return await api<LocationCity[]>('users/cities/').json()
}

export async function registerUserRole(role: User['role']) {
  return await api('users/register/role/', {
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

export async function registerAssociationInfo(associationInfo: UserAssociationInfo) {
  return await api<UserBasicInfo>('users/register/association/', {
    method: 'PATCH',
    json: associationInfo,
  }).json()
}

export interface UserUpdatePayload {
  first_name: string
  last_name: string
  username: string
  location_id: number
  profile_image?: File
  association_name?: string
  association_email?: string
}

export async function updateUserProfile(payload: UserUpdatePayload) {
  const formData = new FormData()
  formData.append('first_name', payload.first_name)
  formData.append('last_name', payload.last_name)
  formData.append('username', payload.username)
  formData.append('location_id', payload.location_id.toString())
  if (payload.profile_image) {
    formData.append('profile_image', payload.profile_image)
  }
  if (payload.association_name) {
    formData.append('association_name', payload.association_name)
  }
  if (payload.association_email) {
    formData.append('association_email', payload.association_email)
  }

  return await api<User>('users/update/', {
    method: 'PATCH',
    body: formData,
  }).json()
}

export async function getUserById(userId: number) {
  return await api<User>(`users/${userId}/`).json()
}