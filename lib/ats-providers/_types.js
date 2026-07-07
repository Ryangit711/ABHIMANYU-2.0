// Type definitions for ATS provider system
// @ts-check

/**
 * @typedef {Object} PortalEntry
 * @property {string} name - Company name
 * @property {string} [careers_url] - Career portal URL
 * @property {string} [api] - API endpoint URL (if direct)
 * @property {string} [provider] - Explicit ATS provider id
 * @property {boolean} [enabled] - Whether to scan this company
 */

/**
 * @typedef {Object} Provider
 * @property {string} id - Unique provider identifier
 * @property {(entry: PortalEntry) => {url: string}|null} detect - Check if this provider handles the entry
 * @property {(entry: PortalEntry, ctx: Object) => Promise<Array<Object>>} fetch - Fetch jobs from provider
 */

export {}
