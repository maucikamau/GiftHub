import ky, { HTTPError } from 'ky'
import { getCSRFToken } from '@/lib/django.ts'

export const BASE_URL = import.meta.env.DEV ? 'http://localhost:8000' : ''

export const api = ky.create({
  prefixUrl: `${BASE_URL}/api/`,
  retry: {
    shouldRetry: ({ error, retryCount }) => {
      if (error instanceof HTTPError && error.response.status === 401) {
        // Retry on 5xx server errors
        sessionStorage.removeItem('csrftoken')
        return retryCount < 3
      }

      return undefined
    },
  },
  hooks: {
    beforeRequest: [
      async (request, options) => {
        if (request.method !== 'GET') {
          // request.headers.set('Content-Type', 'application/json')
          request.headers.set('X-CSRFToken', await getCSRFToken())
        }
      },
    ],
    beforeError: [
      (error) => {
        // You can customize error handling here
        sessionStorage.removeItem('csrftoken')

        return error
      },
    ],
  },
  credentials: import.meta.env.DEV ? 'include' : 'same-origin',
})
