// API Base URL - Update this to match your backend server
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

/**
 * Recommendation API Service
 * Handles all interactions with the Python recommendation backend
 */

/**
 * Get personalized recommendations for a user
 * @param {string} userId - User ID
 * @param {Object} options - Optional parameters
 * @returns {Promise<Array>} Array of recommended products
 */
export const getUserRecommendations = async (userId, options = {}) => {
    try {
        const {
            n = 10,
            minPrice,
            maxPrice,
            minRating,
            diversity = false
        } = options;

        const params = new URLSearchParams({
            n: n.toString(),
            ...(minPrice && { min_price: minPrice.toString() }),
            ...(maxPrice && { max_price: maxPrice.toString() }),
            ...(minRating && { min_rating: minRating.toString() }),
            diversity: diversity.toString()
        });

        const response = await fetch(
            `${API_BASE_URL}/api/recommendations/user/${userId}?${params}`
        );

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.recommendations || [];
    } catch (error) {
        console.error('Error fetching user recommendations:', error);
        return [];
    }
};

/**
 * Get products similar to a given product
 * @param {string} productId - Product ID
 * @param {Object} options - Optional parameters
 * @returns {Promise<Array>} Array of similar products
 */
export const getSimilarProducts = async (productId, options = {}) => {
    try {
        const { n = 10, method = 'hybrid' } = options;

        const params = new URLSearchParams({
            n: n.toString(),
            method
        });

        const response = await fetch(
            `${API_BASE_URL}/api/recommendations/similar/${productId}?${params}`
        );

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.recommendations || [];
    } catch (error) {
        console.error('Error fetching similar products:', error);
        return [];
    }
};

/**
 * Get trending products
 * @param {Object} options - Optional parameters
 * @returns {Promise<Array>} Array of trending products
 */
export const getTrendingProducts = async (options = {}) => {
    try {
        const { n = 10, days = 7 } = options;

        const params = new URLSearchParams({
            n: n.toString(),
            days: days.toString()
        });

        const response = await fetch(
            `${API_BASE_URL}/api/recommendations/trending?${params}`
        );

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.recommendations || [];
    } catch (error) {
        console.error('Error fetching trending products:', error);
        return [];
    }
};

/**
 * Track user-product interaction
 * @param {string} userId - User ID
 * @param {string} productId - Product ID
 * @param {string} interactionType - Type of interaction (view, cart, purchase, rating, wishlist)
 * @param {number} rating - Optional rating (for rating type)
 * @returns {Promise<Object>} Response data
 */
export const trackInteraction = async (userId, productId, interactionType, rating = null) => {
    try {
        const body = {
            user_id: userId,
            product_id: productId,
            interaction_type: interactionType,
            timestamp: new Date().toISOString()
        };

        if (rating !== null) {
            body.rating = rating;
        }

        const response = await fetch(`${API_BASE_URL}/api/interactions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error tracking interaction:', error);
        return null;
    }
};

/**
 * Get all products with optional filtering
 * @param {Object} filters - Filter parameters
 * @returns {Promise<Array>} Array of products
 */
export const getProducts = async (filters = {}) => {
    try {
        const { category, minPrice, maxPrice, minRating } = filters;

        const params = new URLSearchParams({
            ...(category && { category }),
            ...(minPrice && { min_price: minPrice.toString() }),
            ...(maxPrice && { max_price: maxPrice.toString() }),
            ...(minRating && { min_rating: minRating.toString() })
        });

        const response = await fetch(
            `${API_BASE_URL}/api/products?${params}`
        );

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.products || [];
    } catch (error) {
        console.error('Error fetching products:', error);
        return [];
    }
};

/**
 * Trigger model retraining
 * @returns {Promise<Object>} Response data
 */
export const retrainModel = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/retrain`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error retraining model:', error);
        return null;
    }
};

/**
 * Check backend health
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error checking backend health:', error);
        return { status: 'unhealthy', error: error.message };
    }
};

export default {
    getUserRecommendations,
    getSimilarProducts,
    getTrendingProducts,
    trackInteraction,
    getProducts,
    retrainModel,
    checkHealth
};
