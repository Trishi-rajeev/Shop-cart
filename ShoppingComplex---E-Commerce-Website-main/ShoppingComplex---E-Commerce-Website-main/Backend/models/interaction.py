"""
User-Product Interaction model
"""
from datetime import datetime
from typing import Optional

class Interaction:
    """Model for user-product interactions (views, purchases, ratings)"""
    
    INTERACTION_TYPES = ['view', 'cart', 'purchase', 'rating', 'wishlist']
    
    def __init__(
        self,
        user_id: str,
        product_id: str,
        interaction_type: str,
        rating: Optional[float] = None,
        timestamp: Optional[datetime] = None
    ):
        if interaction_type not in self.INTERACTION_TYPES:
            raise ValueError(f"Invalid interaction type. Must be one of {self.INTERACTION_TYPES}")
        
        self.user_id = user_id
        self.product_id = product_id
        self.interaction_type = interaction_type
        self.rating = rating
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self):
        """Convert interaction to dictionary"""
        return {
            'user_id': self.user_id,
            'product_id': self.product_id,
            'interaction_type': self.interaction_type,
            'rating': self.rating,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create interaction from dictionary"""
        return cls(
            user_id=data.get('user_id', ''),
            product_id=data.get('product_id', ''),
            interaction_type=data.get('interaction_type', 'view'),
            rating=data.get('rating'),
            timestamp=datetime.fromisoformat(data['timestamp']) if data.get('timestamp') else None
        )
    
    def __repr__(self):
        return f"Interaction(user={self.user_id}, product={self.product_id}, type={self.interaction_type})"
