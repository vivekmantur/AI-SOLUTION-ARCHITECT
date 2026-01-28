import axios from 'axios';

// API base URL - will use proxy in development, direct URL in production
const API_BASE_URL = process.env.REACT_APP_API_URL || '';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 400000, // 200 seconds for LLM processing
});

// Generate architecture/design
export const generateDesign = async (requirements, cloud) => {
  try {
    const response = await api.post('/design', {
      requirements,
      cloud,
    });
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || error.message,
    };
  }
};

// List available architecture patterns
export const listPatterns = async () => {
  try {
    const response = await api.get('/patterns');
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || error.message,
    };
  }
};

export default api;
