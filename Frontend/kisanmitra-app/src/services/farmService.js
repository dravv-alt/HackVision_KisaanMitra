/**
 * Farm Management API Service
 * Handles planning, farming, and post-harvest operations
 */

import { apiClient } from './api.js';

/**
 * Get pre-seeding crop recommendations
 * @param {object} request - Planning request
 * @param {string} request.farmer_id - Farmer ID (use F001, F002, F003, or F004)
 * @param {string} request.season - Season (kharif/rabi/zaid)
 * @param {object} request.location - Location {state, district}
 * @param {string} request.soil_type - Soil type
 * @param {number} request.farm_size_acres - Farm size in acres
 * @param {boolean} request.irrigation_available - Irrigation availability
 * @returns {Promise<object>} Pre-seeding output with crop and scheme cards
 */
export async function getPreSeedingPlan(request) {
    return await apiClient.post('/planning/pre-seeding', request);
}

/**
 * Detect plant disease from image
 * @param {File} imageFile - Crop image file
 * @returns {Promise<object>} Disease detection result
 * @note Currently may fail due to TensorFlow model compatibility issue
 */
export async function detectDisease(imageFile) {
    const formData = new FormData();
    formData.append('file', imageFile);

    return await apiClient.postFormData('/farming/disease-detect', formData);
}

/**
 * Get market price for a crop
 * @param {string} crop - Crop name
 * @param {string} state - State name (optional)
 * @returns {Promise<object>} Market data with price, trend, demand
 */
export async function getMarketPrice(crop, state = null) {
    const params = { crop };
    if (state) params.state = state;

    return await apiClient.get('/farming/market-price', params);
}

/**
 * Get post-harvest plan (sell vs store, market selection)
 * @param {object} context - Harvest context
 * @param {string} context.crop_name - Crop name
 * @param {number} context.quantity_kg - Quantity in kg
 * @param {array} context.farmer_location - [latitude, longitude]
 * @param {string} context.harvest_date - Harvest date (YYYY-MM-DD)
 * @param {string} context.today_date - Today's date (YYYY-MM-DD)
 * @returns {Promise<object>} Post-harvest plan with recommendations
 */
export async function getPostHarvestPlan(context) {
    return await apiClient.post('/post-harvest/plan', context);
}
