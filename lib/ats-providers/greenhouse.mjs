// Greenhouse ATS Provider
// Hits boards-api.greenhouse.io JSON endpoint
// Auto-detects from greenhouse.io URLs

import { fetchJson } from './_http.mjs'

const ALLOWED_HOSTS = new Set([
  'boards-api.greenhouse.io',
  'boards.greenhouse.io',
  'job-boards.greenhouse.io',
  'job-boards.eu.greenhouse.io',
])

function resolveApiUrl(entry) {
  if (entry.api) return entry.api
  const url = entry.careers_url || ''
  const match = url.match(/job-boards(?:\.eu)?\.greenhouse\.io\/([^/?#]+)/)
  if (match) return `https://boards-api.greenhouse.io/v1/boards/${match[1]}/jobs`
  return null
}

export default {
  id: 'greenhouse',

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
    if (!data || !Array.isArray(data.jobs)) return []

    return data.jobs.map(job => ({
      id: String(job.id),
      title: job.title || '',
      location: job.location?.name || '',
      department: job.metadata?.find(m => m.name === 'Department')?.value || '',
      url: job.absolute_url || '',
      updated_at: job.updated_at || '',
      source: 'greenhouse',
      company: entry.name,
    }))
  },
}
