"""
Example usage of the recommendation system
"""
import requests
import json

# API base URL
BASE_URL = "http://localhost:5000"

def get_user_recommendations(user_id, n=10, min_rating=0.0):
    """Get personalized recommendations for a user"""
    url = f"{BASE_URL}/api/recommendations/user/{user_id}"
    params = {
        'n': n,
        'min_rating': min_rating
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def get_similar_products(product_id, n=10, method='hybrid'):
    """Get similar products"""
    url = f"{BASE_URL}/api/recommendations/similar/{product_id}"
    params = {
        'n': n,
        'method': method
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def get_trending_products(n=10, days=7):
    """Get trending products"""
    url = f"{BASE_URL}/api/recommendations/trending"
    params = {
        'n': n,
        'days': days
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def track_interaction(user_id, product_id, interaction_type, rating=None):
    """Track a user-product interaction"""
    url = f"{BASE_URL}/api/interactions"
    data = {
        'user_id': user_id,
        'product_id': product_id,
        'interaction_type': interaction_type
    }
    
    if rating:
        data['rating'] = rating
    
    response = requests.post(url, json=data)
    if response.status_code == 201:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def main():
    """Example usage"""
    print("=== E-Commerce Recommendation System Examples ===\n")
    
    # 1. Get user recommendations
    print("1. Getting recommendations for user001...")
    user_recs = get_user_recommendations('user001', n=5, min_rating=4.0)
    if user_recs:
        print(f"Found {len(user_recs['recommendations'])} recommendations:")
        for rec in user_recs['recommendations']:
            product = rec['product']
            print(f"  - {product['name']} (Score: {rec['score']:.2f}, Rating: {product['rating']})")
    print()
    
    # 2. Get similar products
    print("2. Getting products similar to prod001...")
    similar = get_similar_products('prod001', n=5, method='hybrid')
    if similar:
        print(f"Found {len(similar['recommendations'])} similar products:")
        for rec in similar['recommendations']:
            product = rec['product']
            print(f"  - {product['name']} (Similarity: {rec['score']:.2f})")
    print()
    
    # 3. Get trending products
    print("3. Getting trending products...")
    trending = get_trending_products(n=5, days=7)
    if trending:
        print(f"Found {len(trending['recommendations'])} trending products:")
        for rec in trending['recommendations']:
            product = rec['product']
            print(f"  - {product['name']} (Trend Score: {rec['score']:.2f})")
    print()
    
    # 4. Track an interaction
    print("4. Tracking a product view...")
    interaction = track_interaction('user001', 'prod005', 'view')
    if interaction:
        print(f"Interaction tracked: {interaction['message']}")
    print()
    
    # 5. Track a purchase with rating
    print("5. Tracking a purchase with rating...")
    purchase = track_interaction('user001', 'prod005', 'purchase', rating=5.0)
    if purchase:
        print(f"Purchase tracked: {purchase['message']}")
    print()

if __name__ == '__main__':
    main()
