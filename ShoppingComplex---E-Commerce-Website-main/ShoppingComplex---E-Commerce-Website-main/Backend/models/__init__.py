"""
Data models for the recommendation system
"""
from .product import Product
from .user import User
from .interaction import Interaction

__all__ = ['Product', 'User', 'Interaction']
