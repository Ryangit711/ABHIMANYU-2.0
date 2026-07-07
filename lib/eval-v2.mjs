// EVAL V2 Scoring Engine — 10-dimension evaluation
// Ported from career-ops process-quality.mjs + OPS_EVAL_CRITERIA.md
// Used before SHOOT to validate resume + cover letter quality

const WEIGHTS = {
  roleFit: 2.0,
  cvMatch: 1.0,
  levelStrategy: 1.0,
  compResearch: 1.0,
  personalization: 1.0,
  interviewPrep: 1.5,
  companyTrajectory: 0.5,
  teamQuality: 0.5,
  location: 0.5,
  ghostCheck: 0.5,
}

const MAX_SCORE = 10 * Object.values(WEIGHTS).reduce((a, b) => a + b, 0) // 95

export function evaluateJob(job, context = {}) {
  const scores = {
    roleFit: scoreRoleFit(job, context),
    cvMatch: scoreCVMatch(job, context),
    levelStrategy: scoreLevelStrategy(job, context),
    compResearch: scoreCompResearch(job, context),
    personalization: scorePersonalization(job, context),
    interviewPrep: scoreInterviewPrep(job, context),
    companyTrajectory: scoreCompanyTrajectory(job, context),
    teamQuality: scoreTeamQuality(job, context),
    location: scoreLocation(job, context),
    ghostCheck: scoreGhostCheck(job, context),
  }

  const rawScore = Object.entries(scores).reduce(
    (sum, [key, score]) => sum + score * WEIGHTS[key],
    0
  )

  const normalized = Math.round((rawScore / MAX_SCORE) * 100)
  const verdict = normalized >= 70 ? 'PASS' : normalized >= 50 ? 'WARN' : 'FAIL'

  const strongest = Object.entries(scores)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 2)
    .map(([key]) => key)

  const weakest = Object.entries(scores)
    .sort(([, a], [, b]) => a - b)
    .slice(0, 2)
    .map(([key]) => key)

  return {
    scores,
    rawScore: Math.round(rawScore * 10) / 10,
    maxScore: MAX_SCORE,
    normalized,
    verdict,
    strongest,
    weakest,
    recommendation: verdict === 'PASS'
      ? 'Proceed with SHOOT'
      : verdict === 'WARN'
        ? 'Rewrite flagged sections and re-evaluate'
        : 'Full rewrite from scratch recommended',
  }
}

function scoreRoleFit(job, context) {
  // Base score: check title + description keywords against Aman's profile
  const title = (job.title || '').toLowerCase()
  const desc = (job.description || '').toLowerCase()

  // Keywords that indicate strong fit
  const strongFit = ['operations', 'strategy', 'director', 'head of', 'chief of staff']
  const moderateFit = ['manager', 'lead', 'program', 'consultant']

  const strongMatches = strongFit.filter(kw => title.includes(kw)).length
  const moderateMatches = moderateFit.filter(kw => title.includes(kw)).length

  const descStrength = desc.includes('scaling') || desc.includes('transformation') ||
    desc.includes('cross-functional') || desc.includes('operations') ? 2 : 0

  let score = 5 + strongMatches * 2 + moderateMatches * 1 + descStrength
  return Math.min(10, Math.max(1, score))
}

function scoreCVMatch(job, context) {
  const resumeText = context.resumeText || ''
  if (!resumeText) return 5

  const desc = (job.description || '').toLowerCase()
  const resumeLower = resumeText.toLowerCase()

  // Count keyword overlap
  const keywords = desc.split(/\s+/).filter(w => w.length > 4)
  const matched = keywords.filter(kw => resumeLower.includes(kw)).length
  const ratio = keywords.length > 0 ? matched / keywords.length : 0.5

  return Math.min(10, Math.round(ratio * 10))
}

function scoreLevelStrategy(job, context) {
  const title = (job.title || '').toLowerCase()
  const salary = job.salary || 0

  // Senior Manager / Director / VP level = best fit
  if (title.includes('vp') || title.includes('director') || title.includes('head of')) {
    return salary >= 120000 ? 9 : 8
  }
  if (title.includes('senior manager') || title.includes('principal')) {
    return salary >= 100000 ? 8 : 7
  }
  if (title.includes('manager') || title.includes('lead')) {
    return salary >= 90000 ? 7 : 6
  }
  if (title.includes('coordinator') || title.includes('analyst') || title.includes('associate')) {
    return 3
  }
  return 5
}

function scoreCompResearch(job, context) {
  const salary = job.salary || context.salary || 0
  if (salary >= 120000) return 8
  if (salary >= 100000) return 7
  if (salary >= 80000) return 6
  if (job.salaryRange) return 5 // range available but no exact
  return 3 // no salary data
}

function scorePersonalization(job, context) {
  const hasCoverLetter = context.hasCoverLetter || false
  const hasCustomResume = context.hasCustomResume || false

  if (hasCoverLetter && hasCustomResume) return 8
  if (hasCoverLetter || hasCustomResume) return 6
  return 4
}

function scoreInterviewPrep(job, context) {
  // Higher score if we have process knowledge for this company
  const company = (job.company || '').toLowerCase()
  const knownProcesses = ['deloitte', 'mckinsey', 'telus', 'lululemon', 'shopify', 'clio']
  const known = knownProcesses.some(kp => company.includes(kp))
  return known ? 7 : 5
}

function scoreCompanyTrajectory(job, context) {
  const news = (context.companyNews || '').toLowerCase()
  if (news.includes('funding') || news.includes('growth') || news.includes('expansion')) return 8
  if (news.includes('layoff') || news.includes('freeze') || news.includes('decline')) return 3
  return 6
}

function scoreTeamQuality(job, context) {
  const reviews = (context.glassdoorReviews || '').toLowerCase()
  if (reviews.includes('great') || reviews.includes('excellent') || reviews.includes('amazing')) return 8
  if (reviews.includes('toxic') || reviews.includes('awful') || reviews.includes('terrible')) return 3
  return 6
}

function scoreLocation(job, context) {
  const location = (job.location || '').toLowerCase()
  if (location.includes('remote') && location.includes('canada')) return 10
  if (location.includes('vancouver') || location.includes('burnaby')) return 9
  if (location.includes('british columbia') || location.includes('bc')) return 8
  if (location.includes('canada')) return 6
  return 2
}

function scoreGhostCheck(job, context) {
  const ghostResult = context.ghostResult || {}
  if (ghostResult.severity === 'safe') return 10
  if (ghostResult.severity === 'suspect') return 5
  if (ghostResult.severity === 'ghost') return 1
  return 8
}
