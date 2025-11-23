"""
Utility functions for data processing and management
"""
import json
import pickle
from typing import List, Dict, Any
from datetime import datetime
import os

class DataManager:
    """Manages loading and saving of data"""
    
    @staticmethod
    def load_json(filepath: str) -> Any:
        """Load data from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {filepath}: {e}")
            return None
    
    @staticmethod
    def save_json(data: Any, filepath: str):
        """Save data to JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_pickle(filepath: str) -> Any:
        """Load data from pickle file"""
        try:
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return None
    
    @staticmethod
    def save_pickle(data: Any, filepath: str):
        """Save data to pickle file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

class CacheManager:
    """Simple in-memory cache manager"""
    
    def __init__(self, ttl: int = 3600):
        """
        Initialize cache manager
        
        Args:
            ttl: Time to live in seconds
        """
        self.cache = {}
        self.ttl = ttl
    
    def get(self, key: str) -> Any:
        """Get value from cache"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if (datetime.now() - timestamp).seconds < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """Set value in cache"""
        self.cache[key] = (value, datetime.now())
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
    
    def delete(self, key: str):
        """Delete specific key from cache"""
        if key in self.cache:
            del self.cache[key]

def normalize_scores(scores: List[tuple], min_score: float = 0.0, max_score: float = 1.0) -> List[tuple]:
    """
    Normalize recommendation scores to a specific range
    
    Args:
        scores: List of (item_id, score) tuples
        min_score: Minimum score value
        max_score: Maximum score value
        
    Returns:
        List of (item_id, normalized_score) tuples
    """
    if not scores:
        return []
    
    # Find min and max scores
    score_values = [s[1] for s in scores]
    current_min = min(score_values)
    current_max = max(score_values)
    
    # Avoid division by zero
    if current_max == current_min:
        return [(item_id, max_score) for item_id, _ in scores]
    
    # Normalize
    normalized = []
    for item_id, score in scores:
        normalized_score = min_score + (score - current_min) * (max_score - min_score) / (current_max - current_min)
        normalized.append((item_id, normalized_score))
    
    return normalized

def merge_recommendations(
    rec_lists: List[List[tuple]],
    weights: List[float] = None,
    n_recommendations: int = 10
) -> List[tuple]:
    """
    Merge multiple recommendation lists with optional weights
    
    Args:
        rec_lists: List of recommendation lists, each containing (item_id, score) tuples
        weights: Optional weights for each list
        n_recommendations: Number of final recommendations
        
    Returns:
        Merged list of (item_id, score) tuples
    """
    if not rec_lists:
        return []
    
    # Default equal weights
    if weights is None:
        weights = [1.0] * len(rec_lists)
    
    # Normalize weights
    total_weight = sum(weights)
    weights = [w / total_weight for w in weights]
    
    # Merge scores
    merged_scores = {}
    for rec_list, weight in zip(rec_lists, weights):
        for item_id, score in rec_list:
            if item_id in merged_scores:
                merged_scores[item_id] += score * weight
            else:
                merged_scores[item_id] = score * weight
    
    # Sort and return top N
    recommendations = sorted(
        merged_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return recommendations[:n_recommendations]

def filter_by_price_range(
    products: List[Dict],
    min_price: float = None,
    max_price: float = None
) -> List[Dict]:
    """
    Filter products by price range
    
    Args:
        products: List of product dictionaries
        min_price: Minimum price
        max_price: Maximum price
        
    Returns:
        Filtered list of products
    """
    filtered = []
    for product in products:
        price = product.get('price', 0)
        if min_price is not None and price < min_price:
            continue
        if max_price is not None and price > max_price:
            continue
        filtered.append(product)
    
    return filtered

def filter_by_rating(
    products: List[Dict],
    min_rating: float = 0.0
) -> List[Dict]:
    """
    Filter products by minimum rating
    
    Args:
        products: List of product dictionaries
        min_rating: Minimum rating
        
    Returns:
        Filtered list of products
    """
    return [p for p in products if p.get('rating', 0) >= min_rating]

def diversity_rerank(
    recommendations: List[tuple],
    products_dict: Dict[str, Dict],
    diversity_factor: float = 0.3,
    category_key: str = 'category'
) -> List[tuple]:
    """
    Re-rank recommendations to increase diversity
    
    Args:
        recommendations: List of (product_id, score) tuples
        products_dict: Dictionary mapping product_id to product data
        diversity_factor: How much to penalize similar categories (0-1)
        category_key: Key to use for diversity (e.g., 'category', 'brand')
        
    Returns:
        Re-ranked list of (product_id, score) tuples
    """
    if not recommendations:
        return []
    
    reranked = []
    seen_categories = {}
    
    for product_id, score in recommendations:
        product = products_dict.get(product_id, {})
        category = product.get(category_key, 'unknown')
        
        # Apply diversity penalty
        if category in seen_categories:
            penalty = diversity_factor * seen_categories[category]
            adjusted_score = score * (1 - penalty)
        else:
            adjusted_score = score
        
        reranked.append((product_id, adjusted_score))
        
        # Update category count
        seen_categories[category] = seen_categories.get(category, 0) + 0.1
    
    # Re-sort by adjusted scores
    reranked.sort(key=lambda x: x[1], reverse=True)
    
    return reranked
