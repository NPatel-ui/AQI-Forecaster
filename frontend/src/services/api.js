import axios from 'axios';

// Vite proxy forwards /api -> http://127.0.0.1:8000
const API_BASE = import.meta.env.VITE_API_URL || '/api';

export const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 8000,
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
    // Also try direct localhost:8000 if proxy failed
    try {
      const direct = await axios.get('http://127.0.0.1:8000/health', { timeout: 3000 });
      return {
        connected: true,
        data: direct.data,
        error: null,
      };
    } catch {
      return {
        connected: false,
        data: null,
        error: err.response?.data?.detail || err.message || 'Backend service unreachable',
      };
    }
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
    // Try direct fallback
    try {
      const params = date ? { date } : {};
      const direct = await axios.get(`http://127.0.0.1:8000/forecast/${encodeURIComponent(city)}`, {
        params,
        timeout: 5000,
      });
      return {
        success: true,
        data: direct.data,
        error: null,
      };
    } catch (secondErr) {
      const message =
        secondErr.response?.data?.detail ||
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
    return {
      success: false,
      data: null,
      error: err.response?.data?.detail || err.message,
    };
  }
}

