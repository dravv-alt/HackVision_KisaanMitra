/**
 * Government Schemes API Service
 * Handles scheme listing and filtering
 */

import { apiClient } from './api.js';

/**
 * Get government schemes (all or filtered)
 * @param {object} filters - Filter options
 * @param {string} filters.category - Scheme category (optional)
 * @param {string} filters.state - State filter (optional)
 * @param {string} filters.district - District filter (optional)
 * @param {boolean} filters.force_refresh - Force refresh from API (optional)
 * @returns {Promise<object>} Government schemes output
 */
export async function getSchemes(filters = {}) {
    return await apiClient.get('/schemes', filters);
}

/**
 * Get specific scheme details
 * @param {string} schemeId - Scheme ID
 * @returns {Promise<object>} Scheme record
 */
export async function getSchemeDetails(schemeId) {
    return await apiClient.get(`/schemes/${schemeId}`);
}
