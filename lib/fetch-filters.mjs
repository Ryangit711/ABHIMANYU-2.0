// FETCH Filter System — ported from career-ops portal.yml
// Used during QBIT 2 (Collapse Wavefunction) to filter jobs

// Title Filter
export const TITLE_FILTER = {
  positive: [
    // Operations & Strategy (core)
    'operations', 'strategy', 'strategic', 'operational',
    // Leadership & General Management
    'director', 'head of', 'vice president', 'vp ', 'president',
    'chief ', 'senior manager', 'manager', 'lead', 'principal', 'partner',
    // Consulting & Advisory
    'consultant', 'consulting', 'advisor', 'advisory',
    // Program & Project Management
    'program', 'project', 'portfolio', 'delivery',
    // Growth & Development
    'growth', 'business development', 'corporate development', 'bd ',
    // Transformation & Change
    'transformation', 'change', 'turnaround', 'restructuring', 'value creation',
    // M&A & Integration
    "m&a", 'merger', 'acquisition', 'integration', 'due diligence',
    // Practice & Engagement (consulting)
    'practice', 'engagement', 'scoping',
    // Architecture (non-technical)
    'architect',
    // Excellence & Quality
    'excellence', 'quality',
    // Process & Optimization
    'process', 'optimization', 'scaling',
    // Innovation & Ventures
    'innovation', 'venture', 'launch',
    // Product-adjacent (ops/strategy side)
    'product operations', 'product strategy', 'product management',
    // Marketing Operations
    'marketing operations', 'marketing strategy', 'growth marketing',
    // People & Talent (senior only)
    'people operations', 'talent operations',
    // Executive & Founder-adjacent
    'coo', 'chief of staff', 'general manager', 'gm ',
    // Revenue & Commercial
    'revenue', 'commercial',
    // Senior IC titles
    'senior associate', 'manager,',
  ],

  negative: [
    // Technical roles
    'engineer', 'engineering', 'software', 'developer', 'programmer',
    'coding', 'full stack', 'fullstack', 'frontend', 'front-end',
    'backend', 'back-end', 'front end', 'back end',
    'devops', 'sre', 'infrastructure', 'platform engineer',
    'data engineer', 'data scientist', 'machine learning', 'ml engineer',
    'ai engineer',
    // Data & Analytics
    'data analyst', 'business intelligence', 'bi analyst', 'analytics engineer',
    // Finance & Accounting
    'financial analyst', 'finance manager', 'accountant', 'accounting',
    'controller', 'tax ', 'audit', 'underwriter', 'actuarial',
    'valuation', 'transfer pricing', 'fp&a', 'treasury', 'comptroller',
    // Banking / Credit
    'credit', 'risk analyst', 'quant',
    // Healthcare licensed
    'veterinary', 'veterinarian', 'nurse', 'nursing', 'pharmacist',
    'pharmacy', 'clinical', 'surgical', 'diagnostic', 'radiologist',
    'therapist', 'counselor', 'psychologist', 'practitioner', 'physician',
    // Admin / Support / Entry-level
    'administrative assistant', 'executive assistant', 'admin assistant',
    'office manager', 'receptionist', 'coordinator', 'intern',
    'junior', 'entry level', 'associate',
    // Sales / Customer Success
    'sales', 'account executive', 'ae ', 'customer success', 'cs manager',
    'support', 'help desk', 'service desk',
    // Security / Legal / Compliance
    'security', 'cyber', 'cybersecurity', 'legal', 'compliance',
    'regulatory', 'paralegal', 'attorney', 'counsel',
    // HR / Recruiting
    'recruiter', 'recruiting', 'hr ', 'hr manager', 'hr business partner',
    'payroll', 'benefits', 'compensation',
    // Procurement / Supply Chain
    'procurement', 'supply chain', 'logistics', 'warehouse',
    // Facilities / Real Estate
    'facilities', 'real estate', 'property',
    // Marketing / Creative (pure)
    'marketing manager', 'content', 'social media', 'brand manager',
    'creative', 'designer', 'graphic', 'seo', 'sem',
    // Communications / PR
    'communications', 'public relations', 'pr ', 'corporate communications',
    // Specialized
    'pilot', 'flight', 'clinic',
    // Banking roles
    'teller', 'branch manager', 'loan', 'mortgage',
    // Graduate / Apprenticeship
    'graduate', 'apprentice', 'trainee', 'new grad',
  ],
}

export const CONTENT_FILTER = {
  positive: [
    'operations', 'strategy', 'strategic', 'operational',
    'transformation', 'cross-functional', 'business operations',
    'program management', 'project management', 'stakeholder',
    'go-to-market', 'scale', 'scaling', 'process improvement',
    'process optimization', 'organizational design', 'change management',
    'operational excellence', 'value creation', 'executive', 'board',
    'M&A', 'merger', 'integration', 'due diligence', 'advisory',
    'consulting', 'consultant', 'growth strategy', 'strategic planning',
    'implementation', 'systems', 'workflow', 'automation', 'efficiency',
    'optimization', 'turnaround', 'restructuring', 'revenue growth',
    'profitability', 'p&l', 'general management', 'chief of staff',
    'coo', 'operating model',
  ],
  negative: [
    'software engineering', 'software development', 'full stack',
    'fullstack', 'data scientist', 'machine learning engineer',
    'devops engineer', 'site reliability', 'clinical', 'surgical',
    'patient care',
  ],
}

// Location filter targeting Vancouver/Remote Canada only
export const LOCATION_FILTER = {
  alwaysAllow: [
    'Vancouver', 'Burnaby', 'Coquitlam', 'Delta', 'Langley',
    'North Vancouver', 'West Vancouver', 'New Westminster',
    'Port Moody', 'Port Coquitlam', 'British Columbia', 'BC',
  ],
  allow: ['Richmond', 'Surrey', 'Remote', 'Canada'],
  block: [
    // Canadian non-BC
    'Ontario', 'Toronto', 'Mississauga', 'Brampton', 'Hamilton',
    'Ottawa', 'Kitchener', 'Waterloo', 'Quebec', 'Montreal',
    'Montréal', 'Quebec City', 'Alberta', 'Calgary', 'Edmonton',
    'Manitoba', 'Winnipeg', 'Saskatchewan', 'Saskatoon', 'Regina',
    'Nova Scotia', 'Halifax', 'New Brunswick', 'PEI', 'Newfoundland',
    'Yukon', 'Northwest Territories', 'Nunavut',
    // US cities/states
    'USA', 'California', 'San Francisco', 'New York', 'Seattle',
    'Texas', 'Austin', 'Massachusetts', 'Boston', 'Illinois',
    'Chicago', 'Florida', 'Miami', 'Virginia', 'Colorado',
    'Denver', 'Oregon', 'Portland', 'Georgia', 'Atlanta',
    'Washington DC', 'DC',
    // International
    'UK', 'United Kingdom', 'London', 'India', 'Bengaluru',
    'Mumbai', 'Australia', 'Sydney', 'Melbourne', 'Singapore',
    'Germany', 'Berlin', 'Munich', 'France', 'Paris',
    'Japan', 'Tokyo', 'Ireland', 'Dublin', 'Netherlands',
    'Amsterdam', 'Switzerland', 'Zurich', 'Spain', 'Madrid',
    'Italy', 'Milan', 'UAE', 'Dubai',
  ],
}

export const SALARY_FILTER = {
  min: 80_000,
  max: 350_000,
  currency: 'CAD',
}

// Ghost/Stale job detection
export function isStaleJob(job) {
  if (!job.updated_at && !job.posted_at) return false

  const dateStr = job.updated_at || job.posted_at
  const postedDate = new Date(dateStr)
  const now = new Date()
  const daysSince = (now - postedDate) / (1000 * 60 * 60 * 24)

  return daysSince > 90
}

// Apply title filter to a job title
export function passesTitleFilter(title) {
  if (!title) return false
  const lower = title.toLowerCase()

  // Check negative first (reject if any match)
  for (const neg of TITLE_FILTER.negative) {
    if (lower.includes(neg)) return false
  }

  // Check positive (pass if any match)
  for (const pos of TITLE_FILTER.positive) {
    if (lower.includes(pos)) return true
  }

  return false
}

// Apply content filter to a job description
export function passesContentFilter(description) {
  if (!description) return true // no description = pass (title filter handles)
  const lower = description.toLowerCase()

  // Check negative
  for (const neg of CONTENT_FILTER.negative) {
    if (lower.includes(neg)) return false
  }

  // Check positive
  for (const pos of CONTENT_FILTER.positive) {
    if (lower.includes(pos)) return true
  }

  return true // pass by default if no positive match in content
}

// Apply location filter
export function passesLocationFilter(location) {
  if (!location) return false
  const lower = location.toLowerCase()

  // Check block list
  for (const block of LOCATION_FILTER.block) {
    if (lower.includes(block.toLowerCase())) return false
  }

  // Check always allow
  for (const allow of LOCATION_FILTER.alwaysAllow) {
    if (lower.includes(allow.toLowerCase())) return true
  }

  // Check conditional allow
  for (const allow of LOCATION_FILTER.allow) {
    if (lower.includes(allow.toLowerCase())) return true
  }

  return false
}

// Master filter function
export function filterJob(job) {
  const reasons = []

  // Title filter
  if (!passesTitleFilter(job.title)) {
    reasons.push(`title: "${job.title}"`)
  }

  // Location filter
  if (!passesLocationFilter(job.location)) {
    reasons.push(`location: "${job.location}"`)
  }

  // Stale check
  if (isStaleJob(job)) {
    reasons.push('stale (>90 days)')
  }

  return {
    passed: reasons.length === 0,
    reasons,
  }
}
