/**
 * API client for communicating with the FastAPI backend.
 * All API calls go through this centralized service.
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Search for products using natural language query.
 * @param {string} query - The search query
 * @param {number} limit - Maximum number of results
 * @returns {Promise} Search results
 */
export const searchProducts = async (query, limit = 10) => {
  const response = await apiClient.post('/search', { query, limit });
  return response.data;
};

/**
 * Get historical sales data for a product.
 * @param {string} articleId - Product article ID
 * @param {number} days - Number of days of history
 * @returns {Promise} Sales data
 */
export const getProductSales = async (articleId, days = 90) => {
  const response = await apiClient.get(`/products/${articleId}/sales`, {
    params: { days }
  });
  return response.data;
};

/**
 * Get demand forecast for a product.
 * @param {string} articleId - Product article ID
 * @param {number} days - Number of days to forecast
 * @returns {Promise} Forecast data
 */
export const getProductForecast = async (articleId, days = 30) => {
  const response = await apiClient.get(`/products/${articleId}/forecast`, {
    params: { days }
  });
  return response.data;
};

/**
 * Get customer segmentation for a product.
 * @param {string} articleId - Product article ID
 * @returns {Promise} Customer segments
 */
export const getCustomerSegments = async (articleId) => {
  const response = await apiClient.get(`/products/${articleId}/segments`);
  return response.data;
};

/**
 * Generate AI insights for a product.
 * @param {string} articleId - Product article ID
 * @param {object} salesData - Optional sales data for context
 * @returns {Promise} AI-generated insights
 */
export const generateInsights = async (articleId, salesData = null) => {
  const response = await apiClient.post('/insights', {
    article_id: articleId,
    sales_data: salesData
  });
  return response.data;
};

export default {
  searchProducts,
  getProductSales,
  getProductForecast,
  getCustomerSegments,
  generateInsights,
};

