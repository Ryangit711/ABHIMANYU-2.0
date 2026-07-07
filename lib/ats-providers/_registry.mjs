// ATS Provider Registry — maps companies to their ATS platform
// Ported from career-ops provider pattern.
// Each provider implements: { id, detect(entry), fetch(entry, ctx) }
//
// Usage:
//   import { resolveProvider, loadProviders } from './_registry.mjs'
//   const providers = await loadProviders('./lib/ats-providers')
//   const { provider } = resolveProvider({ name: 'Shopify', careers_url: '...' }, providers)
//   if (provider) const jobs = await provider.fetch(entry, ctx)

import { existsSync, readdirSync } from 'fs'
import path from 'path'
import { pathToFileURL } from 'url'

export async function loadProviders(dir) {
  const providers = new Map()
  if (!existsSync(dir)) return providers
  const entries = readdirSync(dir)
    .filter(f => f.endsWith('.mjs') && !f.startsWith('_'))
    .sort()
  for (const file of entries) {
    const full = path.join(dir, file)
    let mod
    try {
      mod = await import(pathToFileURL(full).href)
    } catch (err) {
      console.error(`⚠️  ${file}: failed to load — ${err.message}`)
      continue
    }
    const p = mod.default
    if (!p || typeof p.fetch !== 'function' || !p.id) {
      console.error(`⚠️  ${file}: skipping — default export must be { id, fetch }`)
      continue
    }
    if (providers.has(p.id)) {
      console.error(`⚠️  ${file}: duplicate provider id "${p.id}" — keeping first`)
      continue
    }
    providers.set(p.id, p)
  }
  return providers
}

// Company → ATS mapping for known companies (curated from ATS_ESOTERICA.md)
const COMPANY_ATS_MAP = {
  // T Pipe — Tech
  'Shopify': 'greenhouse',
  'Clio': 'workday',
  '1Password': 'ashby',
  'DoorDash': 'greenhouse',
  'Brex': 'greenhouse',
  'Wealthsimple': 'lever',
  'Thinkific': 'greenhouse',
  'Copper': 'greenhouse',
  'Trulioo': 'ashby',
  'Procurify': 'ashby',
  'Ada': 'lever',
  'Hiive': 'lever',
  'EvenUp': 'greenhouse',
  'Indeed': 'icims',
  'Hootsuite': 'icims',
  'Jobber': 'greenhouse',
  // C Pipe — Consulting
  'Deloitte': 'successfactors',
  'EY': 'successfactors',
  'KPMG': 'workday',
  'PwC': 'workday',
  'Accenture': 'workday',
  'McKinsey': 'greenhouse',
  'BCG': 'greenhouse',
  'Bain': 'lever',
  'Slalom': 'custom',
  'Gartner': 'custom',
  'MNP': 'ultipro',
  // I Pipe — Internal Strategy / Corporate
  'TELUS': 'successfactors',
  'Rogers': 'workday',
  'Bell': 'custom',
  'lululemon': 'greenhouse',
  'Aritzia': 'custom',
  'Arc\'teryx': 'workday',
  'BC Hydro': 'custom',
  'Methanex': 'custom',
  'Providence Healthcare': 'custom',
  'Aviso Wealth': 'workable',
  'AECOM': 'smartrecruiters',
  'Amazon': 'amazon',
  'Google': 'custom',
  'Microsoft': 'custom',
  'Marqeta': 'greenhouse',
  'Zenoti': 'greenhouse',
  'SOCi': 'greenhouse',
  'Human Agency': 'greenhouse',
  'OpenTable': 'greenhouse',
  // S Pipe — Startups
  'Practice Better': 'greenhouse',
  'EviSmart': 'greenhouse',
  'Remarcable': 'custom',
}

export function resolveProvider(entry, providers) {
  // 1. Check explicit provider field
  if (entry.provider) {
    const p = providers.get(entry.provider)
    if (p) return { provider: p }
    return { error: `unknown provider: ${entry.provider}` }
  }

  // 2. Check company name in map
  const atsId = COMPANY_ATS_MAP[entry.name]
  if (atsId) {
    const p = providers.get(atsId)
    if (p) return { provider: p }
  }

  // 3. Try auto-detect from URL
  for (const p of providers.values()) {
    try {
      const hit = p.detect?.(entry)
      if (hit) return { provider: p }
    } catch { continue }
  }

  return { error: 'no matching provider' }
}
