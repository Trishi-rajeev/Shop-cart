"""
Hybrid Recommender
Combines collaborative filtering and content-based approaches
"""
from typing import List, Dict, Tuple
from .collaborative_filtering import CollaborativeFilteringRecommender
from .content_based import ContentBasedRecommender

class HybridRecommender:
    """
    Hybrid recommendation system combining collaborative and content-based filtering
    """
    
    def __init__(
        self,
        collaborative_weight: float = 0.6,
        content_weight: float = 0.4
    ):
        """
        Initialize hybrid recommender
        
        Args:
            collaborative_weight: Weight for collaborative filtering (0-1)
            content_weight: Weight for content-based filtering (0-1)
        """
        # Normalize weights
        total = collaborative_weight + content_weight
        self.collaborative_weight = collaborative_weight / total
        self.content_weight = content_weight / total
        
        self.collaborative_recommender = CollaborativeFilteringRecommender()
        self.content_recommender = ContentBasedRecommender()
        
        self.is_fitted = False
    
    def fit(self, products: List[Dict], interactions: List[Dict]):
        """
        Train both recommendation models
        
        Args:
            products: List of product dictionaries
            interactions: List of interaction dictionaries
        """
        # Train collaborative filtering model
        if interactions:
            self.collaborative_recommender.fit(interactions)
        
        # Train content-based model
        if products:
            self.content_recommender.fit(products)
        
        self.is_fitted = True
        return self
    
    def recommend(
        self,
        user_id: str,
        user_preferences: List[str] = None,
        user_interactions: List[Dict] = None,
        n_recommendations: int = 10,
        exclude_interacted: bool = True
    ) -> List[Tuple[str, float]]:
        """
        Generate hybrid recommendations for a user
        
        Args:
            user_id: Target user ID
            user_preferences: User's category/tag preferences
            user_interactions: User's interaction history
            n_recommendations: Number of recommendations to return
            exclude_interacted: Whether to exclude already interacted products
            
        Returns:
            List of (product_id, score) tuples
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making recommendations")
        
        # Get collaborative filtering recommendations
        collab_recs = self.collaborative_recommender.recommend_item_based(
            user_id=user_id,
            n_recommendations=n_recommendations * 2,
            exclude_interacted=exclude_interacted
        )
        
        # Get content-based recommendations
        content_recs = []
        if user_preferences or user_interactions:
            content_recs = self.content_recommender.recommend_for_user(
                user_preferences=user_preferences or [],
                user_interactions=user_interactions or [],
                n_recommendations=n_recommendations * 2,
                exclude_interacted=exclude_interacted
            )
        
        # Combine recommendations
        combined_scores = {}
        
        # Add collaborative filtering scores
        for product_id, score in collab_recs:
            combined_scores[product_id] = score * self.collaborative_weight
        
        # Add content-based scores
        for product_id, score in content_recs:
            if product_id in combined_scores:
                combined_scores[product_id] += score * self.content_weight
            else:
                combined_scores[product_id] = score * self.content_weight
        
        # Sort by combined score
        recommendations = sorted(
            combined_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return recommendations[:n_recommendations]
    
    def recommend_similar_products(
        self,
        product_id: str,
        n_recommendations: int = 10,
        use_collaborative: bool = True,
        use_content: bool = True
    ) -> List[Tuple[str, float]]:
        """
        Recommend products similar to a given product
        
        Args:
            product_id: Target product ID
            n_recommendations: Number of recommendations to return
            use_collaborative: Use collaborative filtering
            use_content: Use content-based filtering
            
        Returns:
            List of (product_id, score) tuples
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making recommendations")
        
        combined_scores = {}
        
        # Get collaborative filtering similar products
        if use_collaborative:
            collab_similar = self.collaborative_recommender.get_similar_products(
                product_id=product_id,
                n_similar=n_recommendations * 2
            )
            for prod_id, score in collab_similar:
                combined_scores[prod_id] = score * self.collaborative_weight
        
        # Get content-based similar products
        if use_content:
            content_similar = self.content_recommender.recommend_similar_products(
                product_id=product_id,
                n_recommendations=n_recommendations * 2
            )
            for prod_id, score in content_similar:
                if prod_id in combined_scores:
                    combined_scores[prod_id] += score * self.content_weight
                else:
                    combined_scores[prod_id] = score * self.content_weight
        
        # Sort by combined score
        recommendations = sorted(
            combined_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return recommendations[:n_recommendations]
    
    def recommend_trending(
        self,
        interactions: List[Dict],
        time_window_days: int = 7,
        n_recommendations: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Recommend trending products based on recent interactions
        
        Args:
            interactions: List of recent interactions
            time_window_days: Time window in days for trending calculation
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of (product_id, score) tuples
        """
        from datetime import datetime, timedelta
        from collections import defaultdict
        
        # Calculate cutoff time
        cutoff_time = datetime.now() - timedelta(days=time_window_days)
        
        # Count interactions per product with weights
        product_scores = defaultdict(float)
        
        for interaction in interactions:
            # Check if within time window
            timestamp = interaction.get('timestamp')
            if timestamp:
                if isinstance(timestamp, str):
                    timestamp = datetime.fromisoformat(timestamp)
                if timestamp < cutoff_time:
                    continue
            
            product_id = interaction['product_id']
            
            # Weight different interaction types
            if interaction.get('interaction_type') == 'purchase':
                weight = 5.0
            elif interaction.get('interaction_type') == 'cart':
                weight = 3.0
            elif interaction.get('interaction_type') == 'wishlist':
                weight = 2.0
            else:
                weight = 1.0
            
            product_scores[product_id] += weight
        
        # Sort by score
        trending = sorted(
            product_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return trending[:n_recommendations]
