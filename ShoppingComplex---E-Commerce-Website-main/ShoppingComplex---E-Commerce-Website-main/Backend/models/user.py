"""
User data model
"""
from datetime import datetime
from typing import List, Optional

class User:
    """User model for customers"""
    
    def __init__(
        self,
        user_id: str,
        username: str,
        email: str,
        preferences: Optional[List[str]] = None,
        purchase_history: Optional[List[str]] = None,
        viewed_products: Optional[List[str]] = None,
        created_at: Optional[datetime] = None
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.preferences = preferences or []
        self.purchase_history = purchase_history or []
        self.viewed_products = viewed_products or []
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'preferences': self.preferences,
            'purchase_history': self.purchase_history,
            'viewed_products': self.viewed_products,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create user from dictionary"""
        return cls(
            user_id=data.get('user_id', ''),
            username=data.get('username', ''),
            email=data.get('email', ''),
            preferences=data.get('preferences'),
            purchase_history=data.get('purchase_history'),
            viewed_products=data.get('viewed_products'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
    
    def __repr__(self):
        return f"User(id={self.user_id}, username={self.username})"
