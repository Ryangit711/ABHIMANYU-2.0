// @ts-check
/** @typedef {import('./_types.js').Provider} Provider */

// Startup Jobs provider — uses the free public API at api.startup.jobs/v1.
// Requires an API key (free at https://startup.jobs/account/api_keys).
// Configure via:
//   1. STARTUP_JOBS_API_KEY env var, or
//   2. entry.api_key in portals.yml under the job_boards entry
//   3. Falls back to the `api_key` query param (discouraged but works)
//
// Wire in via a `job_boards:` entry with `provider: startupjobs` and
// optionally `api_key: sj_your_key_here`.

const API_BASE = 'https://api.startup.jobs/v1';

function resolveApiKey(entry) {
  return entry?.api_key || process.env.STARTUP_JOBS_API_KEY || '';
}

function buildHeaders(apiKey) {
  const headers = { Accept: 'application/json' };
  if (apiKey) headers.Authorization = `Bearer ${apiKey}`;
  return headers;
}

function sanitiseUrl(url) {
  if (!url || typeof url !== 'string') return '';
  try {
    const parsed = new URL(url);
    return parsed.protocol === 'https:' ? parsed.href : '';
  } catch {
    return '';
  }
}

function formatLocation(location) {
  if (!location || typeof location !== 'object') return '';
  const parts = [location.city, location.state, location.country].filter(Boolean);
  return parts.join(', ');
}

function parseDate(value) {
  if (typeof value === 'string') {
    const parsed = Date.parse(value);
    return Number.isNaN(parsed) ? undefined : parsed;
  }
  return undefined;
}

/** @type {Provider} */
export default {
  id: 'startupjobs',

  async fetch(entry, ctx) {
    const apiKey = resolveApiKey(entry);
    const params = new URLSearchParams({
      q: 'operations strategy manager director program chief of staff',
      employment_type: 'full-time',
      limit: '50',
    });

    const url = `${API_BASE}/jobs?${params.toString()}`;
    const headers = buildHeaders(apiKey);

    let json;
    try {
      json = await ctx.fetchJson(url, { headers, redirect: 'error' });
    } catch (err) {
      if (!apiKey) return [];
      throw err;
    }

    if (!json || typeof json !== 'object') return [];
    const jobs = Array.isArray(json.data) ? json.data : [];
    if (jobs.length === 0) return [];

    return jobs
      .filter(j => j && typeof j === 'object' && typeof j.title === 'string' && j.title.trim())
      .map(j => {
        const jobUrl = sanitiseUrl(j.url) || `https://startup.jobs/jobs/${j.id}`;
        return {
          title: j.title.trim(),
          url: jobUrl,
          company: j.company?.name || 'Startup',
          location: formatLocation(j.location),
          salary: j.salary || '',
          postedAt: parseDate(j.published_at),
        };
      });
  },
};
