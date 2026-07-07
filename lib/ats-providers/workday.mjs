// Workday ATS Provider
// Uses Workday's public API endpoint
// Auto-detects from workday URLs (*.myworkdayjobs.com, *.wd3.myworkdayjobs.com, etc.)
// Note: Workday APIs vary by tenant. This is a best-effort parser.

import { fetchJson } from './_http.mjs'

const WORKDAY_PATTERNS = [
  /wd\d*\.myworkdayjobs\.com\/([^/?#]+)/,
  /myworkdayjobs\.com\/([^/?#]+)/,
  /workday\.com\/careers\/([^/?#]+)/,
]

function buildApiUrl(entry) {
  if (entry.api) return entry.api
  const url = entry.careers_url || ''
  for (const pattern of WORKDAY_PATTERNS) {
    const match = url.match(pattern)
    if (match) {
      const tenant = match[1]
      return `https://${tenant}.wd3.myworkdayjobs.com/wday/cxs/${tenant}/jobs`
    }
  }
  return null
}

export default {
  id: 'workday',

  detect(entry) {
    try {
      const apiUrl = buildApiUrl(entry)
      return apiUrl ? { url: apiUrl } : null
    } catch {
      return null
    }
  },

  async fetch(entry, ctx) {
    const apiUrl = buildApiUrl(entry)
    if (!apiUrl) return []

    // Workday uses POST for their search API
    const data = await fetchJson(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ limit: 50, offset: 0 }),
    })
    if (!data || !data.jobPostings) return []

    return data.jobPostings.map(job => ({
      id: job.id || '',
      title: job.title || '',
      location: job.location || '',
      department: job.jobFamily || '',
      url: job.url || `${apiUrl.replace('/wday/cxs/', '/jobs/')}/${job.id}`,
      updated_at: job.updatedAt || '',
      source: 'workday',
      company: entry.name,
    }))
  },
}
