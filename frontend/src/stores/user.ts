import type { User } from '@/types/user.ts'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getMe } from '@/api/user.ts'

export const useUserStore = defineStore('user', () => {
  const user = ref<User>()

  // Initial fetch of user data
  // TODO: use vue-query??
  const getCurrentUser = async () => {
    if (user.value)
      return Promise.resolve(user.value)

    const res = await getMe()
    return user.value = res
  }

  return { user, getCurrentUser }
})
