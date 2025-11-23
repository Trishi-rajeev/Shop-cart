"""
Content-Based Recommender
Uses product features to recommend similar items
"""
import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

class ContentBasedRecommender:
    """
    Content-based recommendation system
    Recommends products based on product features and user preferences
    """
    
    def __init__(self):
        """Initialize the content-based recommender"""
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.product_features = None
        self.product_similarity = None
        self.product_ids = []
        self.products_dict = {}
        
    def _create_product_text(self, product: Dict) -> str:
        """
        Create text representation of product for TF-IDF
        
        Args:
            product: Product dictionary
            
        Returns:
            Combined text representation
        """
        parts = []
        
        # Add name (with higher weight by repeating)
        if product.get('name'):
            parts.append(product['name'] * 3)
        
        # Add category (with higher weight)
        if product.get('category'):
            parts.append(product['category'] * 2)
        
        # Add brand
        if product.get('brand'):
            parts.append(product['brand'] * 2)
        
        # Add description
        if product.get('description'):
            parts.append(product['description'])
        
        # Add tags
        if product.get('tags'):
            parts.append(' '.join(product['tags']))
        
        return ' '.join(parts)
    
    def fit(self, products: List[Dict]):
        """
        Train the content-based model
        
        Args:
            products: List of product dictionaries
        """
        self.products_dict = {p['product_id']: p for p in products}
        self.product_ids = [p['product_id'] for p in products]
        
        # Create text representations
        product_texts = [self._create_product_text(p) for p in products]
        
        # Calculate TF-IDF features
        self.product_features = self.tfidf_vectorizer.fit_transform(product_texts)
        
        # Calculate product similarity matrix
        self.product_similarity = cosine_similarity(self.product_features)
        
        return self
    
    def recommend_similar_products(
        self,
        product_id: str,
        n_recommendations: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Recommend products similar to a given product
        
        Args:
            product_id: Target product ID
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of (product_id, similarity_score) tuples
        """
        if product_id not in self.product_ids:
            return []
        
        product_idx = self.product_ids.index(product_id)
        similarities = self.product_similarity[product_idx]
        
        # Create recommendations
        recommendations = []
        for idx, score in enumerate(similarities):
            if idx != product_idx and score > 0:
                recommendations.append((self.product_ids[idx], float(score)))
        
        # Sort by similarity and return top N
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:n_recommendations]
    
    def recommend_for_user(
        self,
        user_preferences: List[str],
        user_interactions: List[Dict],
        n_recommendations: int = 10,
        exclude_interacted: bool = True
    ) -> List[Tuple[str, float]]:
        """
        Recommend products based on user preferences and interaction history
        
        Args:
            user_preferences: List of preferred categories/tags
            user_interactions: List of user's product interactions
            n_recommendations: Number of recommendations to return
            exclude_interacted: Whether to exclude already interacted products
            
        Returns:
            List of (product_id, score) tuples
        """
        # Build user profile from interactions
        interacted_products = defaultdict(float)
        
        for interaction in user_interactions:
            product_id = interaction['product_id']
            
            # Weight different interaction types
            if interaction.get('interaction_type') == 'purchase':
                weight = 5.0
            elif interaction.get('interaction_type') == 'cart':
                weight = 3.0
            elif interaction.get('interaction_type') == 'wishlist':
                weight = 2.5
            elif interaction.get('rating'):
                weight = float(interaction['rating'])
            else:
                weight = 1.0
            
            interacted_products[product_id] = max(
                interacted_products[product_id],
                weight
            )
        
        # Calculate user profile as weighted average of product features
        user_profile = np.zeros(self.product_features.shape[1])
        total_weight = 0
        
        for product_id, weight in interacted_products.items():
            if product_id in self.product_ids:
                product_idx = self.product_ids.index(product_id)
                user_profile += self.product_features[product_idx].toarray()[0] * weight
                total_weight += weight
        
        if total_weight > 0:
            user_profile /= total_weight
        
        # Add preference boost
        if user_preferences:
            preference_text = ' '.join(user_preferences)
            preference_features = self.tfidf_vectorizer.transform([preference_text])
            user_profile += preference_features.toarray()[0] * 0.3
        
        # Calculate similarity to all products
        user_profile_reshaped = user_profile.reshape(1, -1)
        similarities = cosine_similarity(user_profile_reshaped, self.product_features)[0]
        
        # Get interacted products to exclude
        interacted_set = set(interacted_products.keys()) if exclude_interacted else set()
        
        # Create recommendations
        recommendations = []
        for idx, score in enumerate(similarities):
            product_id = self.product_ids[idx]
            if score > 0 and product_id not in interacted_set:
                recommendations.append((product_id, float(score)))
        
        # Sort by score and return top N
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:n_recommendations]
    
    def recommend_by_category(
        self,
        category: str,
        n_recommendations: int = 10,
        min_rating: float = 0.0
    ) -> List[str]:
        """
        Recommend top products in a specific category
        
        Args:
            category: Product category
            n_recommendations: Number of recommendations to return
            min_rating: Minimum product rating
            
        Returns:
            List of product IDs
        """
        # Filter products by category and rating
        category_products = []
        
        for product_id in self.product_ids:
            product = self.products_dict[product_id]
            if (product.get('category', '').lower() == category.lower() and
                product.get('rating', 0) >= min_rating):
                category_products.append((
                    product_id,
                    product.get('rating', 0),
                    product.get('num_ratings', 0)
                ))
        
        # Sort by rating and number of ratings
        category_products.sort(
            key=lambda x: (x[1], x[2]),
            reverse=True
        )
        
        return [p[0] for p in category_products[:n_recommendations]]
