// Ghost Job Detection — ported from career-ops check-liveness.mjs + liveness-core.mjs
// Flags jobs that are likely stale, ghosted, or reposted

// Check if a job is stale based on posting date
export function isStalePosting(job) {
  const dateStr = job.updated_at || job.posted_at || job.datePosted
  if (!dateStr) return { isStale: false, reason: null }

  const postedDate = new Date(dateStr)
  const now = new Date()
  const daysSince = (now - postedDate) / (1000 * 60 * 60 * 24)

  if (daysSince > 90) {
    return { isStale: true, reason: `Posted ${Math.floor(daysSince)} days ago (>90 day threshold)` }
  }
  if (daysSince > 60) {
    return { isStale: true, reason: `Posted ${Math.floor(daysSince)} days ago — likely filled` }
  }

  return { isStale: false, reason: null }
}

// Check if a role was reposted (same title, different date = suspicious)
export function isReposted(job, recentJobs) {
  if (!recentJobs || !job.title) return false

  const sameTitle = recentJobs.filter(j =>
    j.title?.toLowerCase() === job.title?.toLowerCase() &&
    j.company === job.company
  )

  if (sameTitle.length > 1) {
    const dates = sameTitle.map(j => new Date(j.updated_at || j.posted_at))
    const uniqueDates = new Set(dates.map(d => d.toISOString().slice(0, 10)))
    if (uniqueDates.size > 1) return true
  }

  return false
}

// Check for known hiring freeze signals
const FREEZE_KEYWORDS = [
  'hiring freeze', 'layoff', 'restructuring', 'workforce reduction',
  'headcount freeze', 'cost cutting', 'reduction in force',
]

export function hasFreezeSignals(companyNews) {
  if (!companyNews) return { frozen: false, signals: [] }
  const lower = companyNews.toLowerCase()
  const signals = FREEZE_KEYWORDS.filter(kw => lower.includes(kw))
  return {
    frozen: signals.length > 0,
    signals,
  }
}

// Liveness verification — checks if a job URL still resolves
export async function verifyLiveness(jobUrl) {
  if (!jobUrl) return { alive: false, reason: 'no URL' }

  try {
    const controller = new AbortController()
    const timer = setTimeout(() => controller.abort(), 5000)

    const res = await fetch(jobUrl, {
      method: 'HEAD',
      signal: controller.signal,
      redirect: 'follow',
    })
    clearTimeout(timer)

    if (res.status === 200) return { alive: true, reason: null }
    if (res.status === 404) return { alive: false, reason: '404 — job page not found' }
    if (res.status === 301 || res.status === 302) {
      // Redirect could mean the job moved — verify
      return { alive: true, reason: 'redirected' }
    }
    return { alive: false, reason: `HTTP ${res.status}` }
  } catch (err) {
    return { alive: false, reason: err.message }
  }
}

// Full ghost check for a job
export async function ghostCheck(job, context = {}) {
  const checks = []

  // 1. Staleness check
  const stale = isStalePosting(job)
  checks.push({ check: 'staleness', passed: !stale.isStale, detail: stale.reason })

  // 2. Repost check
  const reposted = isReposted(job, context.recentJobs || [])
  checks.push({ check: 'repost', passed: !reposted, detail: reposted ? 'Same title reposted with new date' : null })

  // 3. URL liveness (optional — network call)
  // const live = await verifyLiveness(job.url)
  // checks.push({ check: 'url_liveness', passed: live.alive, detail: live.reason })

  // 4. Freeze check
  if (context.companyNews) {
    const freeze = hasFreezeSignals(context.companyNews)
    checks.push({ check: 'hiring_freeze', passed: !freeze.frozen, detail: freeze.signals.join(', ') })
  }

  const allPassed = checks.every(c => c.passed)
  const severity = allPassed ? 'safe' : checks.filter(c => !c.passed).length <= 1 ? 'suspect' : 'ghost'

  return {
    job: job.title,
    company: job.company,
    severity,
    checks,
    flags: checks.filter(c => !c.passed).map(c => c.check),
  }
}
