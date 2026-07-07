// HTTP transport helpers for ATS API calls
// Ported from career-ops _http.mjs

const DEFAULT_TIMEOUT_MS = 10_000
const DEFAULT_USER_AGENT = 'Mozilla/5.0 (compatible; ABHIMANYU-2.0/1.0)'

async function fetchWithTimeout(url, { timeoutMs = DEFAULT_TIMEOUT_MS, headers = {}, method = 'GET', body = null, redirect = 'follow' } = {}) {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)
  try {
    const res = await fetch(url, {
      method,
      headers: { 'user-agent': DEFAULT_USER_AGENT, ...headers },
      body,
      redirect,
      signal: controller.signal,
    })
    if (!res.ok) {
      const responseText = await res.text().catch(() => '')
      const err = new Error(`HTTP ${res.status} ${res.statusText || ''}`)
      err.status = res.status
      err.body = responseText
      err.retryAfter = res.headers.get('retry-after')
      throw err
    }
    return res
  } finally {
    clearTimeout(timer)
  }
}

export async function fetchJson(url, opts = {}) {
  const res = await fetchWithTimeout(url, opts)
  return await res.json()
}

export async function fetchText(url, opts = {}) {
  const res = await fetchWithTimeout(url, opts)
  return await res.text()
}

export function makeHttpCtx() {
  return { transport: 'http', fetchJson, fetchText }
}
