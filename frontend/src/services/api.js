import axios from 'axios';

// Deployed backend service URL on Render
const DEPLOYED_BACKEND_URL = 'https://aqi-forecaster-qxxn.onrender.com';

// Local development fallback only
const LOCAL_BACKEND_URL = 'http://127.0.0.1:8000';

// Determine API base URL:
// 1. Explicit VITE_API_URL from environment variables (if provided)
// 2. Local development: use '/api' (handled by Vite dev proxy) or localhost
// 3. Production: deployed Render backend URL
const rawEnvUrl = import.meta.env.VITE_API_URL?.trim();
export const API_BASE = rawEnvUrl
  ? rawEnvUrl.replace(/\/$/, '')
  : import.meta.env.DEV
  ? '/api'
  : DEPLOYED_BACKEND_URL;

export const apiClient = axios.create({
  baseURL: API_BASE,
  // 30-second timeout to safely accommodate Render free-tier cold starts
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Check backend health status
 */
export async function checkBackendHealth() {
  try {
    const response = await apiClient.get('/health');
    return {
      connected: true,
      data: response.data,
      error: null,
    };
  } catch (err) {
    // Only attempt direct localhost fallback during local development
    if (import.meta.env.DEV) {
      try {
        const direct = await axios.get(`${LOCAL_BACKEND_URL}/health`, { timeout: 3000 });
        return {
          connected: true,
          data: direct.data,
          error: null,
        };
      } catch {
        // Fall through to error reporting
      }
    }

    return {
      connected: false,
      data: null,
      error: err.response?.data?.detail || err.message || 'Backend service unreachable',
    };
  }
}

/**
 * Fetch forecast for an eligible city and optional date
 * @param {string} city - Eligible Indian city
 * @param {string} [date] - YYYY-MM-DD format (within 2015-01-01 to 2020-07-01)
 */
export async function getCityForecast(city, date = null) {
  try {
    const params = {};
    if (date) params.date = date;

    const response = await apiClient.get(`/forecast/${encodeURIComponent(city)}`, { params });
    return {
      success: true,
      data: response.data,
      error: null,
    };
  } catch (err) {
    // Only attempt direct localhost fallback during local development
    if (import.meta.env.DEV) {
      try {
        const params = date ? { date } : {};
        const direct = await axios.get(`${LOCAL_BACKEND_URL}/forecast/${encodeURIComponent(city)}`, {
          params,
          timeout: 5000,
        });
        return {
          success: true,
          data: direct.data,
          error: null,
        };
      } catch {
        // Fall through to error reporting
      }
    }

    const message =
      err.response?.data?.detail ||
      err.message ||
      'Failed to connect to forecasting model API';
    return {
      success: false,
      data: null,
      error: message,
    };
  }
}

/**
 * Manual prediction endpoint
 */
export async function postManualPredict(features) {
  try {
    const response = await apiClient.post('/predict', features);
    return {
      success: true,
      data: response.data,
      error: null,
    };
  } catch (err) {
    // Only attempt direct localhost fallback during local development
    if (import.meta.env.DEV) {
      try {
        const direct = await axios.post(`${LOCAL_BACKEND_URL}/predict`, features, { timeout: 5000 });
        return {
          success: true,
          data: direct.data,
          error: null,
        };
      } catch {
        // Fall through to error reporting
      }
    }

    return {
      success: false,
      data: null,
      error: err.response?.data?.detail || err.message,
    };
  }
}
