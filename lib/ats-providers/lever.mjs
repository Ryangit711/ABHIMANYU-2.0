// Lever ATS Provider
// Uses Lever's public API endpoint
// Auto-detects from jobs.lever.co URLs

import { fetchJson } from './_http.mjs'

function resolveApiUrl(entry) {
  if (entry.api) return entry.api
  const url = entry.careers_url || ''
  const match = url.match(/jobs\.lever\.co\/([^/?#]+)/)
  if (match) return `https://api.lever.co/v0/postings/${match[1]}`
  return null
}

export default {
  id: 'lever',

  detect(entry) {
    try {
      const apiUrl = resolveApiUrl(entry)
      return apiUrl ? { url: apiUrl } : null
    } catch {
      return null
    }
  },

  async fetch(entry, ctx) {
    const apiUrl = resolveApiUrl(entry)
    if (!apiUrl) return []

    const data = await fetchJson(apiUrl)
    if (!Array.isArray(data)) return []

    return data.map(job => ({
      id: job.id || '',
      title: job.text || '',
      location: job.categories?.location || '',
      department: job.categories?.team || '',
      url: job.hostedUrl || '',
      updated_at: job.createdAt || '',
      source: 'lever',
      company: entry.name,
    }))
  },
}
