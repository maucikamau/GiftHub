import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const user = ref({
    id: 'test',
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@example.com',
    role: { id: 'donor', name: 'Donor' },
    permissions: [
      'donations.can_view_own',
      'donations.can_create',
      'donations.can_update_own',
      'donations.can_delete_own',
      '',
    ],
  })

  return { user }
})
