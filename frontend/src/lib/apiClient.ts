import ky, { HTTPError } from 'ky'
import { getCSRFToken } from '@/lib/django.ts'

export const BASE_URL = import.meta.env.DEV ? 'http://localhost:8000' : ''

export const api = ky.create({
  prefixUrl: `${BASE_URL}/api/`,
  retry: {
    shouldRetry: async ({ error, retryCount }) => {
      if (error instanceof HTTPError && error.response.status === 401) {
        // Retry on 5xx server errors
        const errMsg = await error.response.text()
        if (errMsg.toLowerCase().includes('csrf')) {
          console.error('CSRF token invalid, retrying request...')
          sessionStorage.removeItem('csrftoken')
          return retryCount < 2
        }

        return undefined
      }

      return undefined
    },
  },
  hooks: {
    beforeRequest: [
      async (request) => {
        if (request.method !== 'GET') {
          request.headers.set('X-CSRFToken', await getCSRFToken())
        }
      },
    ],
  },
  credentials: import.meta.env.DEV ? 'include' : 'same-origin',
})
