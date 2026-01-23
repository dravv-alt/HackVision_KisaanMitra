/**
 * Financial Tracking API Service
 * Handles income, expenses, and P&L reports
 */

import { apiClient } from './api.js';

/**
 * Get financial report (P&L)
 * @param {string} season - Season (default: kharif)
 * @param {string} language - Language (hi/en, default: hi)
 * @returns {Promise<object>} Finance module output with P&L and suggestions
 */
export async function getFinanceReport(season = 'kharif', language = 'hi') {
    return await apiClient.get('/finance/report', { season, language });
}

/**
 * Add expense transaction
 * @param {object} data - Transaction data
 * @param {string} data.season - Season
 * @param {string} data.category - Expense category
 * @param {number} data.amount - Amount
 * @param {string} data.notes - Notes (optional)
 * @param {string} data.relatedCropId - Related crop ID (optional)
 * @returns {Promise<object>} Created transaction
 */
export async function addExpense(data) {
    return await apiClient.post('/finance/expense', data);
}

/**
 * Add income transaction
 * @param {object} data - Transaction data
 * @param {string} data.season - Season
 * @param {string} data.category - Income category
 * @param {number} data.amount - Amount
 * @param {string} data.notes - Notes (optional)
 * @param {string} data.relatedCropId - Related crop ID (optional)
 * @returns {Promise<object>} Created transaction
 */
export async function addIncome(data) {
    return await apiClient.post('/finance/income', data);
}
