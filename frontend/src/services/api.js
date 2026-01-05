/**
 * API Service
 * 
 * Module này cung cấp các methods để gọi REST API.
 * Base URL được cấu hình qua environment variable hoặc proxy.
 */

// Base URL - trong Docker, Nginx proxy /api -> backend
const API_BASE = '/api';

/**
 * Wrapper cho fetch với error handling
 * @param {string} endpoint - API endpoint (bắt đầu bằng /)
 * @param {Object} options - Fetch options
 * @returns {Promise<Response>} Response object
 * @throws {Error} Với message từ API hoặc HTTP status
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  
  if (!response.ok) {
    // Cố gắng lấy error message từ response
    let errorMessage = `HTTP ${response.status}`;
    try {
      const text = await response.text();
      if (text) {
        // API có thể trả về JSON error hoặc plain text
        try {
          const json = JSON.parse(text);
          errorMessage = json.detail || json.message || text;
        } catch {
          errorMessage = text;
        }
      }
    } catch {
      // Ignore parse errors
    }
    throw new Error(errorMessage);
  }
  
  return response;
}

/**
 * GET request, trả về raw text (XML)
 * @param {string} endpoint - API endpoint
 * @returns {Promise<string>} Response text
 */
export async function get(endpoint) {
  const response = await apiRequest(endpoint, { method: 'GET' });
  return response.text();
}

/**
 * POST request với JSON body
 * @param {string} endpoint - API endpoint
 * @param {Object} data - Request body
 * @returns {Promise<string>} Response text (XML)
 */
export async function post(endpoint, data) {
  const response = await apiRequest(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  });
  return response.text();
}

/**
 * PUT request với JSON body
 * @param {string} endpoint - API endpoint
 * @param {Object} data - Request body
 * @returns {Promise<string>} Response text (XML)
 */
export async function put(endpoint, data) {
  const response = await apiRequest(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
  return response.text();
}

/**
 * DELETE request
 * @param {string} endpoint - API endpoint
 * @returns {Promise<void>}
 */
export async function del(endpoint) {
  await apiRequest(endpoint, { method: 'DELETE' });
}
