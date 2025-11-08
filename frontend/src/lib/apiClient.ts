import ky from 'ky'
import { getCSRFToken } from '@/lib/django.ts'

export const BASE_URL = import.meta.env.DEV ? 'http://localhost:8000' : ''

export const api = ky.create({
  prefixUrl: `${BASE_URL}/api/`,
  hooks: {
    beforeRequest: [
      async (request, options) => {
        if (request.method !== 'GET') {
          request.headers.set('X-CSRFToken', await getCSRFToken())
        }
      },
    ],
  },
  credentials: 'include', // if you need cookies
})
