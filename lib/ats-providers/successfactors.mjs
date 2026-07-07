// SAP SuccessFactors ATS Provider
// Uses SuccessFactors' public API
// Auto-detects from careers.*.com URLs with SuccessFactors patterns

import { fetchJson, fetchText } from './_http.mjs'

const SF_PATTERNS = [
  /careers\.(\w+)\.com\/?/,
  /jobs\.(\w+)\.com\/?/,
]

function detect(entry) {
  const url = entry.careers_url || ''
  // SuccessFactors URLs typically have specific query params or structure
  // This is a best-effort detection
  for (const pattern of SF_PATTERNS) {
    if (pattern.test(url)) return { url }
  }
  return null
}

export default {
  id: 'successfactors',

  detect(entry) {
    try {
      return detect(entry)
    } catch {
      return null
    }
  },

  async fetch(entry, ctx) {
    const careerUrl = entry.careers_url
    if (!careerUrl) return []

    // SuccessFactors doesn't have a consistent public JSON API
    // For now, return the career URL for manual/referral fetch
    // This will be enhanced with Playwright-based scraping
    return [{
      id: `sf-${entry.name}`,
      title: '',
      location: '',
      department: '',
      url: careerUrl,
      updated_at: '',
      source: 'successfactors',
      company: entry.name,
      note: 'SuccessFactors — requires Playwright scraping or manual fetch',
    }]
  },
}
