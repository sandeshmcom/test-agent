import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 2 minutes timeout for AI generation
});

// Request interceptor
api.interceptors.request.use((config) => {
  console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`);
  return config;
});

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const checkProviders = async () => {
  try {
    const response = await api.get('/providers');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to check providers');
  }
};

export const getTestTypes = async () => {
  try {
    const response = await api.get('/test-types');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to get test types');
  }
};

export const getApplicationTypes = async () => {
  try {
    const response = await api.get('/application-types');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to get application types');
  }
};

export const generateTestCases = async (requestData) => {
  try {
    const response = await api.post('/generate', requestData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to generate test cases');
  }
};

export const exportTestCases = async (format) => {
  try {
    const response = await api.get(`/export/${format}`, {
      responseType: 'blob',
    });
    
    // Create blob link to download
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    
    // Get filename from Content-Disposition header or create default
    const contentDisposition = response.headers['content-disposition'];
    let filename = `test_cases_${new Date().toISOString().split('T')[0]}.${format}`;
    
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="(.+)"/);
      if (filenameMatch) {
        filename = filenameMatch[1];
      }
    }
    
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
    
    return { success: true, filename };
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to export test cases');
  }
};

export const clearTestCases = async () => {
  try {
    const response = await api.delete('/clear');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to clear test cases');
  }
};

export default api;