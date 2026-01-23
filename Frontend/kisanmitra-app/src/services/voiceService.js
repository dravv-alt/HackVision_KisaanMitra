/**
 * Voice Agent API Service
 * Handles text and audio voice interactions
 */

import { apiClient } from './api.js';

/**
 * Process text input through voice agent
 * @param {string} hindiText - Hindi text input
 * @param {string} farmerId - Farmer ID (optional)
 * @param {string} sessionId - Session ID (optional)
 * @returns {Promise<object>} Agent response with cards and explanations
 */
export async function processText(hindiText, farmerId = null, sessionId = null) {
    const payload = {
        hindi_text: hindiText,
    };

    if (farmerId) payload.farmer_id = farmerId;
    if (sessionId) payload.session_id = sessionId;

    return await apiClient.post('/voice/process', payload);
}

/**
 * Process audio file through voice agent
 * @param {File} audioFile - Audio file (wav, mp3, m4a)
 * @param {string} farmerId - Farmer ID (optional)
 * @param {string} sessionId - Session ID (optional)
 * @returns {Promise<object>} Agent response with cards and explanations
 */
export async function processAudio(audioFile, farmerId = null, sessionId = null) {
    const formData = new FormData();
    formData.append('audio', audioFile);

    if (farmerId) formData.append('farmer_id', farmerId);
    if (sessionId) formData.append('session_id', sessionId);

    return await apiClient.postFormData('/voice/process-audio', formData);
}
