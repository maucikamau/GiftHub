export const SESSION_CACHE_PREFIX = 'app_cache_'

const cacheProviders = new Map<string, any>()

export async function cached(key: string, fn: () => Promise<string>) {
  if (cacheProviders.has(key) && cacheProviders.get(key) !== fn) {
    console.warn(`Cache key collision for key "${key}". Overwriting existing cache provider.`)
  }
  const fullKey = SESSION_CACHE_PREFIX + key
  cacheProviders.set(fullKey, fn)
  const cachedValue = sessionStorage.getItem(fullKey)
  if (cachedValue) {
    return cachedValue
  }

  const value = await fn()
  sessionStorage.setItem(fullKey, value)
  return value
}

export async function invalidateSessionCache(key: string) {
  sessionStorage.removeItem(SESSION_CACHE_PREFIX + key)
}
