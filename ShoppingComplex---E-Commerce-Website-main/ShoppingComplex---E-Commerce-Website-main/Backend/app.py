"""
Flask REST API for the recommendation system
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config
from models import Product, User, Interaction
from recommender import HybridRecommender
from utils import DataManager, CacheManager, normalize_scores, diversity_rerank

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Enable CORS
CORS(app, origins=app.config['CORS_ORIGINS'])

# Initialize components
data_manager = DataManager()
cache_manager = CacheManager(ttl=app.config['CACHE_TTL'])
recommender = HybridRecommender(
    collaborative_weight=app.config['COLLABORATIVE_WEIGHT'],
    content_weight=app.config['CONTENT_WEIGHT']
)

# Global data storage (in production, use a proper database)
products_data = []
interactions_data = []
users_data = []

# Load initial data
def load_data():
    """Load data from files"""
    global products_data, interactions_data, users_data
    
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    # Load products
    products_file = os.path.join(data_dir, 'products.json')
    loaded_products = data_manager.load_json(products_file)
    if loaded_products:
        products_data = loaded_products
    
    # Load interactions
    interactions_file = os.path.join(data_dir, 'interactions.json')
    loaded_interactions = data_manager.load_json(interactions_file)
    if loaded_interactions:
        interactions_data = loaded_interactions
    
    # Load users
    users_file = os.path.join(data_dir, 'users.json')
    loaded_users = data_manager.load_json(users_file)
    if loaded_users:
        users_data = loaded_users
    
    # Train recommender if we have data
    if products_data and interactions_data:
        try:
            recommender.fit(products_data, interactions_data)
            print("Recommender system trained successfully!")
        except Exception as e:
            print(f"Error training recommender: {e}")

# API Routes

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'products_count': len(products_data),
        'interactions_count': len(interactions_data),
        'users_count': len(users_data)
    })

@app.route('/api/recommendations/user/<user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    """
    Get personalized recommendations for a user
    
    Query parameters:
    - n: Number of recommendations (default: 10)
    - min_price: Minimum price filter
    - max_price: Maximum price filter
    - min_rating: Minimum rating filter
    - diversity: Enable diversity re-ranking (true/false)
    """
    try:
        # Get parameters
        n = int(request.args.get('n', 10))
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        min_rating = request.args.get('min_rating', type=float, default=0.0)
        enable_diversity = request.args.get('diversity', 'false').lower() == 'true'
        
        # Check cache
        cache_key = f"user_recs_{user_id}_{n}_{min_price}_{max_price}_{min_rating}_{enable_diversity}"
        if app.config['CACHE_ENABLED']:
            cached = cache_manager.get(cache_key)
            if cached:
                return jsonify(cached)
        
        # Get user data
        user_data = next((u for u in users_data if u['user_id'] == user_id), None)
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        # Get user interactions
        user_interactions = [i for i in interactions_data if i['user_id'] == user_id]
        
        # Get recommendations
        recommendations = recommender.recommend(
            user_id=user_id,
            user_preferences=user_data.get('preferences', []),
            user_interactions=user_interactions,
            n_recommendations=n * 2,  # Get more for filtering
            exclude_interacted=True
        )
        
        # Get product details and apply filters
        products_dict = {p['product_id']: p for p in products_data}
        filtered_recs = []
        
        for product_id, score in recommendations:
            product = products_dict.get(product_id)
            if not product:
                continue
            
            # Apply filters
            if min_price and product.get('price', 0) < min_price:
                continue
            if max_price and product.get('price', float('inf')) > max_price:
                continue
            if product.get('rating', 0) < min_rating:
                continue
            
            filtered_recs.append((product_id, score))
        
        # Apply diversity re-ranking if requested
        if enable_diversity:
            filtered_recs = diversity_rerank(filtered_recs, products_dict)
        
        # Normalize scores and limit to n
        filtered_recs = normalize_scores(filtered_recs[:n])
        
        # Build response
        result = {
            'user_id': user_id,
            'recommendations': [
                {
                    'product_id': product_id,
                    'score': score,
                    'product': products_dict.get(product_id)
                }
                for product_id, score in filtered_recs
            ]
        }
        
        # Cache result
        if app.config['CACHE_ENABLED']:
            cache_manager.set(cache_key, result)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/similar/<product_id>', methods=['GET'])
def get_similar_products(product_id):
    """
    Get products similar to a given product
    
    Query parameters:
    - n: Number of recommendations (default: 10)
    - method: 'collaborative', 'content', or 'hybrid' (default: hybrid)
    """
    try:
        n = int(request.args.get('n', 10))
        method = request.args.get('method', 'hybrid')
        
        # Check cache
        cache_key = f"similar_{product_id}_{n}_{method}"
        if app.config['CACHE_ENABLED']:
            cached = cache_manager.get(cache_key)
            if cached:
                return jsonify(cached)
        
        # Get recommendations based on method
        if method == 'collaborative':
            recommendations = recommender.recommend_similar_products(
                product_id=product_id,
                n_recommendations=n,
                use_collaborative=True,
                use_content=False
            )
        elif method == 'content':
            recommendations = recommender.recommend_similar_products(
                product_id=product_id,
                n_recommendations=n,
                use_collaborative=False,
                use_content=True
            )
        else:  # hybrid
            recommendations = recommender.recommend_similar_products(
                product_id=product_id,
                n_recommendations=n
            )
        
        # Normalize scores
        recommendations = normalize_scores(recommendations)
        
        # Get product details
        products_dict = {p['product_id']: p for p in products_data}
        
        result = {
            'product_id': product_id,
            'method': method,
            'recommendations': [
                {
                    'product_id': pid,
                    'score': score,
                    'product': products_dict.get(pid)
                }
                for pid, score in recommendations
            ]
        }
        
        # Cache result
        if app.config['CACHE_ENABLED']:
            cache_manager.set(cache_key, result)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/trending', methods=['GET'])
def get_trending_products():
    """
    Get trending products
    
    Query parameters:
    - n: Number of recommendations (default: 10)
    - days: Time window in days (default: 7)
    """
    try:
        n = int(request.args.get('n', 10))
        days = int(request.args.get('days', 7))
        
        # Check cache
        cache_key = f"trending_{n}_{days}"
        if app.config['CACHE_ENABLED']:
            cached = cache_manager.get(cache_key)
            if cached:
                return jsonify(cached)
        
        # Get trending products
        trending = recommender.recommend_trending(
            interactions=interactions_data,
            time_window_days=days,
            n_recommendations=n
        )
        
        # Get product details
        products_dict = {p['product_id']: p for p in products_data}
        
        result = {
            'time_window_days': days,
            'recommendations': [
                {
                    'product_id': product_id,
                    'score': score,
                    'product': products_dict.get(product_id)
                }
                for product_id, score in trending
            ]
        }
        
        # Cache result
        if app.config['CACHE_ENABLED']:
            cache_manager.set(cache_key, result)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/interactions', methods=['POST'])
def add_interaction():
    """
    Add a new user-product interaction
    
    Request body:
    {
        "user_id": "user123",
        "product_id": "prod456",
        "interaction_type": "view|cart|purchase|rating|wishlist",
        "rating": 4.5 (optional, for rating type)
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('user_id') or not data.get('product_id') or not data.get('interaction_type'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create interaction
        interaction = {
            'user_id': data['user_id'],
            'product_id': data['product_id'],
            'interaction_type': data['interaction_type'],
            'rating': data.get('rating'),
            'timestamp': data.get('timestamp')
        }
        
        # Add to interactions
        interactions_data.append(interaction)
        
        # Clear cache for this user
        cache_manager.delete(f"user_recs_{data['user_id']}")
        
        # Retrain recommender (in production, do this periodically)
        if len(interactions_data) % 100 == 0:  # Retrain every 100 interactions
            recommender.fit(products_data, interactions_data)
        
        return jsonify({
            'message': 'Interaction added successfully',
            'interaction': interaction
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Get all products with optional filtering
    
    Query parameters:
    - category: Filter by category
    - min_price: Minimum price
    - max_price: Maximum price
    - min_rating: Minimum rating
    """
    try:
        category = request.args.get('category')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        min_rating = request.args.get('min_rating', type=float, default=0.0)
        
        # Filter products
        filtered = products_data
        
        if category:
            filtered = [p for p in filtered if p.get('category', '').lower() == category.lower()]
        
        if min_price:
            filtered = [p for p in filtered if p.get('price', 0) >= min_price]
        
        if max_price:
            filtered = [p for p in filtered if p.get('price', float('inf')) <= max_price]
        
        if min_rating:
            filtered = [p for p in filtered if p.get('rating', 0) >= min_rating]
        
        return jsonify({
            'count': len(filtered),
            'products': filtered
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/retrain', methods=['POST'])
def retrain_model():
    """Retrain the recommendation model"""
    try:
        recommender.fit(products_data, interactions_data)
        cache_manager.clear()
        
        return jsonify({
            'message': 'Model retrained successfully',
            'products_count': len(products_data),
            'interactions_count': len(interactions_data)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Initialize data on startup
load_data()

if __name__ == '__main__':
    app.run(
        host=app.config['API_HOST'],
        port=app.config['API_PORT'],
        debug=app.config['DEBUG']
    )
