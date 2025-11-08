import type { OAuthProviders } from '@/types/auth'
import { BASE_URL } from '@/lib/apiClient.ts'
import { getCSRFToken } from '@/lib/django.ts'

const settings = {
  baseUrl: `${BASE_URL}/_allauth/browser/v1`,
}

function postForm(action: string, data: Record<string, any>) {
  const f = document.createElement('form')
  f.method = 'POST'
  f.action = settings.baseUrl + action

  for (const key in data) {
    const d = document.createElement('input')
    d.type = 'hidden'
    d.name = key
    d.value = data[key]
    f.appendChild(d)
  }
  document.body.appendChild(f)
  f.submit()
}

export async function loginWithOauth(provider: OAuthProviders) {
  // redirect user to backend oauth endpoint
  // make a POST request to /_allauth/
  const payload = {
    provider,
    process: 'login',
    callback_url: `${window.location.protocol}//${window.location.host}`,
    csrfmiddlewaretoken: await getCSRFToken(),
  }

  // console.log(payload)

  postForm('/auth/provider/redirect', payload)
}
