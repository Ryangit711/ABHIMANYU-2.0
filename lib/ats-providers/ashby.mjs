// Ashby ATS Provider
// Uses Ashby's public API endpoint
// Auto-detects from jobs.ashbyhq.com URLs

import { fetchJson } from './_http.mjs'

function resolveApiUrl(entry) {
  if (entry.api) return entry.api
  const url = entry.careers_url || ''
  const match = url.match(/jobs\.ashbyhq\.com\/([^/?#]+)/)
  if (match) return `https://jobs.ashbyhq.com/${match[1]}`
  return null
}

export default {
  id: 'ashby',

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

    const data = await fetchJson(`${apiUrl}/api/non/user/content`)
    if (!data || !data.jobs) return []

    return data.jobs.map(job => ({
      id: job.id || '',
      title: job.title || '',
      location: job.location || '',
      department: job.department || '',
      url: `${apiUrl}/job/${job.id}`,
      updated_at: job.publishedDate || '',
      source: 'ashby',
      company: entry.name,
    }))
  },
}
