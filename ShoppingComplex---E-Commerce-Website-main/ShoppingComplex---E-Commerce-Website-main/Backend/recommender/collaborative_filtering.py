"""
Collaborative Filtering Recommender
Uses user-item interactions to find similar users and recommend products
"""
import numpy as np
from typing import List, Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

class CollaborativeFilteringRecommender:
    """
    Collaborative filtering recommendation system
    Supports both user-based and item-based collaborative filtering
    """
    
    def __init__(self, min_common_items: int = 2):
        """
        Initialize the collaborative filtering recommender
        
        Args:
            min_common_items: Minimum number of common items for similarity calculation
        """
        self.min_common_items = min_common_items
        self.user_item_matrix = None
        self.item_user_matrix = None
        self.user_similarity = None
        self.item_similarity = None
        self.user_ids = []
        self.product_ids = []
        
    def fit(self, interactions: List[Dict]):
        """
        Train the collaborative filtering model
        
        Args:
            interactions: List of interaction dictionaries with user_id, product_id, and rating
        """
        # Build user-item matrix
        user_product_ratings = defaultdict(lambda: defaultdict(float))
        
        for interaction in interactions:
            user_id = interaction['user_id']
            product_id = interaction['product_id']
            
            # Assign weights based on interaction type
            if interaction.get('interaction_type') == 'purchase':
                rating = 5.0
            elif interaction.get('interaction_type') == 'cart':
                rating = 4.0
            elif interaction.get('interaction_type') == 'wishlist':
                rating = 3.5
            elif interaction.get('interaction_type') == 'view':
                rating = 2.0
            elif interaction.get('rating'):
                rating = float(interaction['rating'])
            else:
                rating = 1.0
            
            # Take the maximum rating if multiple interactions exist
            user_product_ratings[user_id][product_id] = max(
                user_product_ratings[user_id][product_id],
                rating
            )
        
        # Create sorted lists of user and product IDs
        self.user_ids = sorted(user_product_ratings.keys())
        all_products = set()
        for products in user_product_ratings.values():
            all_products.update(products.keys())
        self.product_ids = sorted(all_products)
        
        # Create user-item matrix
        self.user_item_matrix = np.zeros((len(self.user_ids), len(self.product_ids)))
        
        for i, user_id in enumerate(self.user_ids):
            for j, product_id in enumerate(self.product_ids):
                self.user_item_matrix[i, j] = user_product_ratings[user_id].get(product_id, 0)
        
        # Calculate user similarity matrix
        self.user_similarity = cosine_similarity(self.user_item_matrix)
        
        # Calculate item similarity matrix
        self.item_similarity = cosine_similarity(self.user_item_matrix.T)
        
        return self
    
    def recommend_user_based(
        self,
        user_id: str,
        n_recommendations: int = 10,
        exclude_interacted: bool = True
    ) -> List[Tuple[str, float]]:
        """
        Generate recommendations using user-based collaborative filtering
        
        Args:
            user_id: Target user ID
            n_recommendations: Number of recommendations to return
            exclude_interacted: Whether to exclude already interacted products
            
        Returns:
            List of (product_id, score) tuples
        """
        if user_id not in self.user_ids:
            return []
        
        user_idx = self.user_ids.index(user_id)
        
        # Get similar users
        user_similarities = self.user_similarity[user_idx]
        
        # Calculate predicted ratings
        predicted_ratings = np.zeros(len(self.product_ids))
        
        for product_idx in range(len(self.product_ids)):
            # Get users who interacted with this product
            product_ratings = self.user_item_matrix[:, product_idx]
            
            # Calculate weighted average of ratings from similar users
            numerator = np.sum(user_similarities * product_ratings)
            denominator = np.sum(np.abs(user_similarities) * (product_ratings > 0))
            
            if denominator > 0:
                predicted_ratings[product_idx] = numerator / denominator
        
        # Get user's interacted products
        user_interacted = set()
        if exclude_interacted:
            user_interacted = {
                self.product_ids[i]
                for i in range(len(self.product_ids))
                if self.user_item_matrix[user_idx, i] > 0
            }
        
        # Create recommendations
        recommendations = []
        for product_idx, score in enumerate(predicted_ratings):
            product_id = self.product_ids[product_idx]
            if score > 0 and product_id not in user_interacted:
                recommendations.append((product_id, float(score)))
        
        # Sort by score and return top N
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:n_recommendations]
    
    def recommend_item_based(
        self,
        user_id: str,
        n_recommendations: int = 10,
        exclude_interacted: bool = True
    ) -> List[Tuple[str, float]]:
        """
        Generate recommendations using item-based collaborative filtering
        
        Args:
            user_id: Target user ID
            n_recommendations: Number of recommendations to return
            exclude_interacted: Whether to exclude already interacted products
            
        Returns:
            List of (product_id, score) tuples
        """
        if user_id not in self.user_ids:
            return []
        
        user_idx = self.user_ids.index(user_id)
        user_ratings = self.user_item_matrix[user_idx]
        
        # Calculate scores for all products
        predicted_ratings = np.dot(user_ratings, self.item_similarity)
        
        # Normalize by sum of similarities
        similarity_sums = np.sum(self.item_similarity * (user_ratings > 0)[:, np.newaxis], axis=0)
        similarity_sums[similarity_sums == 0] = 1  # Avoid division by zero
        predicted_ratings = predicted_ratings / similarity_sums
        
        # Get user's interacted products
        user_interacted = set()
        if exclude_interacted:
            user_interacted = {
                self.product_ids[i]
                for i in range(len(self.product_ids))
                if user_ratings[i] > 0
            }
        
        # Create recommendations
        recommendations = []
        for product_idx, score in enumerate(predicted_ratings):
            product_id = self.product_ids[product_idx]
            if score > 0 and product_id not in user_interacted:
                recommendations.append((product_id, float(score)))
        
        # Sort by score and return top N
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:n_recommendations]
    
    def get_similar_products(
        self,
        product_id: str,
        n_similar: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Find similar products based on user interactions
        
        Args:
            product_id: Target product ID
            n_similar: Number of similar products to return
            
        Returns:
            List of (product_id, similarity_score) tuples
        """
        if product_id not in self.product_ids:
            return []
        
        product_idx = self.product_ids.index(product_id)
        similarities = self.item_similarity[product_idx]
        
        # Create list of similar products
        similar_products = []
        for idx, score in enumerate(similarities):
            if idx != product_idx and score > 0:
                similar_products.append((self.product_ids[idx], float(score)))
        
        # Sort by similarity and return top N
        similar_products.sort(key=lambda x: x[1], reverse=True)
        return similar_products[:n_similar]
