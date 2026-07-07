// Contact Discovery — ported from career-ops contacto mode
// Finds hiring manager, recruiter, team peer, and executive contacts
// for a target company. Outputs structured contact map + outreach drafts.

// Known company contacts (curated from past SHOOT packages + manual research)
// Format: { name, title, linkedin_url, tier, context }
// Tiers: HM (Hiring Manager), SR (Senior Recruiter), 
//        TP (Team Peer), EX (Executive)

const KNOWN_CONTACTS = {
  // T Pipe
  'Clio': [
    { name: '', title: 'VP People', tier: 'EX', context: 'Oversight of all hiring', linkedin_url: '' },
    { name: '', title: 'Recruiter', tier: 'SR', context: 'Tech/ops roles', linkedin_url: '' },
  ],
  'Shopify': [
    { name: '', title: 'Talent Acquisition Lead', tier: 'SR', context: 'Operations roles', linkedin_url: '' },
    { name: '', title: 'VP Operations', tier: 'EX', context: 'Reporting structure', linkedin_url: '' },
  ],
  '1Password': [
    { name: '', title: 'People Team Lead', tier: 'SR', context: 'All hiring', linkedin_url: '' },
    { name: '', title: 'Chief Revenue Officer', tier: 'EX', context: 'If RevOps role', linkedin_url: '' },
  ],
  // C Pipe
  'Deloitte': [
    { name: '', title: 'Partner, Strategy & Ops', tier: 'EX', context: 'Practice lead', linkedin_url: '' },
    { name: '', title: 'Senior Recruiter', tier: 'SR', context: 'S&O practice hiring', linkedin_url: '' },
  ],
  'McKinsey': [
    { name: '', title: 'Engagement Manager', tier: 'HM', context: 'Potential skip-level', linkedin_url: '' },
    { name: '', title: 'Recruiting Manager', tier: 'SR', context: 'Experienced hiring', linkedin_url: '' },
  ],
  // I Pipe
  'TELUS': [
    { name: '', title: 'Director, Strategy', tier: 'HM', context: 'Internal strategy team', linkedin_url: '' },
    { name: '', title: 'Talent Acquisition Partner', tier: 'SR', context: 'Corporate roles', linkedin_url: '' },
  ],
  'lululemon': [
    { name: '', title: 'Sr Manager, Strategy', tier: 'HM', context: 'Potential direct report', linkedin_url: '' },
    { name: '', title: 'Talent Acquisition', tier: 'SR', context: 'Ops roles', linkedin_url: '' },
  ],
  // S Pipe
  'Brex': [
    { name: '', title: 'Head of Operations', tier: 'EX', context: 'Potential skip', linkedin_url: '' },
    { name: '', title: 'Recruiter', tier: 'SR', context: 'Scale-up hiring', linkedin_url: '' },
  ],
  'Hiive': [
    { name: '', title: 'CEO / Founder', tier: 'EX', context: 'Direct to founder', linkedin_url: '' },
    { name: '', title: 'Chief of Staff', tier: 'TP', context: 'Potential peer', linkedin_url: '' },
  ],
}

export function getContacts(companyName) {
  return KNOWN_CONTACTS[companyName] || [
    // Default contact tiers for unknown companies
    { name: '', title: 'Hiring Manager', tier: 'HM', context: 'Direct supervisor for the role', linkedin_url: '' },
    { name: '', title: 'Recruiter / Talent Acquisition', tier: 'SR', context: 'Screening and process', linkedin_url: '' },
    { name: '', title: 'Team Peer / IC', tier: 'TP', context: 'Potential cultural fit insight', linkedin_url: '' },
    { name: '', title: 'Department Executive', tier: 'EX', context: 'Strategic context', linkedin_url: '' },
  ]
}

// Generate contact tiers and outreach strategy
export function generateContactStrategy(companyName, role) {
  const contacts = getContacts(companyName)

  // Group by tier
  const tiers = {
    HM: contacts.filter(c => c.tier === 'HM'),
    SR: contacts.filter(c => c.tier === 'SR'),
    TP: contacts.filter(c => c.tier === 'TP'),
    EX: contacts.filter(c => c.tier === 'EX'),
  }

  return {
    company: companyName,
    role,
    tiers,
    suggestedCadence: [
      { day: 0, action: 'Connect on LinkedIn', target: 'HM', message: generateConnectMessage('HM', companyName, role) },
      { day: 3, action: 'Send follow-up / engage', target: 'SR', message: generateEngageMessage('SR', companyName, role) },
      { day: 7, action: 'Value-add note', target: 'TP', message: generateValueAddMessage('TP', companyName, role) },
      { day: 14, action: 'Check-in nudge', target: 'HM', message: generateNudgeMessage('HM', companyName, role) },
      { day: 28, action: 'Final close', target: 'EX', message: generateCloseMessage('EX', companyName, role) },
    ],
  }
}

function generateConnectMessage(tier, company, role) {
  const templates = {
    HM: `Hi — I recently applied for the ${role} role. I've been following ${company}'s work in the space and would love to connect.`,
    SR: `Hi — I applied for the ${role} position and wanted to introduce myself. My background is scaling operations from 3→70, $17M exit — seems aligned with what you're building.`,
    TP: `Hi — I'm exploring the ${role} role at ${company}. Would love to learn about your experience on the team.`,
    EX: `Hello — I have deep respect for ${company}'s trajectory. I'd welcome the chance to connect.`,
  }
  return templates[tier] || ''
}

function generateEngageMessage(tier, company, role) {
  return `Following up on my application for ${role}. Happy to share more about how I built the operations backbone for a US medical roll-up (3→70 team, $17M exit).`
}

function generateValueAddMessage(tier, company, role) {
  return `Came across [relevant article/insight] and thought of ${company}'s current work on [initiative]. Wanted to share in case useful.`
}

function generateNudgeMessage(tier, company, role) {
  return `Just checking in on the ${role} role. Still very interested in ${company} and how my operations background could support your team's goals.`
}

function generateCloseMessage(tier, company, role) {
  return `Wanted to do one last check on the ${role} role. If it's closed or went another direction, completely understand. Wishing ${company} the best.`
}

// Web search prompt for live contact discovery
export function buildContactSearchPrompt(companyName) {
  return `Find people at ${companyName} who could be contacts for a job application.
Look for: hiring manager for operations/strategy roles, recruiters, team members, executives.
Search TheOrg.com, LinkedIn, company leadership page, news mentions. Return names + titles + LinkedIn URLs.`
}
