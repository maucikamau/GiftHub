import type { OAuthProviders } from '@/types/auth'
import ky from 'ky'
import { BASE_URL } from '@/lib/apiClient.ts'
import { getCSRFToken } from '@/lib/django.ts'
import { qc } from '@/lib/vueQuery.ts'

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

  // invalidate csrf token, it changes on user login/logout
  sessionStorage.removeItem('csrftoken')

  postForm('/auth/provider/redirect', payload)
}

export async function loginWithEmail(email: string, password: string) {
  const payload = {
    email,
    password,
  }
  const result = await ky.post(`${settings.baseUrl}/auth/login`, {
    json: payload,
    headers: { 'X-CSRFToken': await getCSRFToken() },
    credentials: 'include',
  }).json().catch(async (error) => {
    console.error('Login failed', error)
    const errMsg = await error.response.json().then(data => data.errors.map(e => e.message).join('<br/>'))
    throw new Error(errMsg)
  })

  // invalidate csrf token, it changes on user login/logout
  sessionStorage.removeItem('csrftoken')

  // invalidate user query
  await qc.invalidateQueries(['users'])

  return result
}

export async function signupWithEmail(email: string, password: string) {
  const payload = {
    email,
    password,
  }
  const result = await ky.post(`${settings.baseUrl}/auth/signup`, {
    json: payload,
    headers: { 'X-CSRFToken': await getCSRFToken() },
    credentials: 'include',
  }).json().catch(async (error) => {
    console.error('Signup failed', error)
    const data = await error.response.json()
    const err = new Error(data.errors.map(e => e.message).join('\n'))
    err.detail = data.errors
    throw err
  })

  // invalidate csrf token, it changes on user login/logout
  sessionStorage.removeItem('csrftoken')

  // invalidate user query
  await qc.invalidateQueries(['users'])

  return result
}
