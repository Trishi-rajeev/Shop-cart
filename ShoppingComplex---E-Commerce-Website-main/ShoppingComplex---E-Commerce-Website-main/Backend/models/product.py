"""
Product data model
"""
from datetime import datetime
from typing import List, Optional

class Product:
    """Product model for e-commerce items"""
    
    def __init__(
        self,
        product_id: str,
        name: str,
        category: str,
        price: float,
        description: Optional[str] = None,
        brand: Optional[str] = None,
        tags: Optional[List[str]] = None,
        image_url: Optional[str] = None,
        rating: float = 0.0,
        num_ratings: int = 0,
        stock: int = 0,
        created_at: Optional[datetime] = None
    ):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.description = description or ""
        self.brand = brand or ""
        self.tags = tags or []
        self.image_url = image_url or ""
        self.rating = rating
        self.num_ratings = num_ratings
        self.stock = stock
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'product_id': self.product_id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'description': self.description,
            'brand': self.brand,
            'tags': self.tags,
            'image_url': self.image_url,
            'rating': self.rating,
            'num_ratings': self.num_ratings,
            'stock': self.stock,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create product from dictionary"""
        return cls(
            product_id=data.get('product_id', ''),
            name=data.get('name', ''),
            category=data.get('category', ''),
            price=data.get('price', 0.0),
            description=data.get('description'),
            brand=data.get('brand'),
            tags=data.get('tags'),
            image_url=data.get('image_url'),
            rating=data.get('rating', 0.0),
            num_ratings=data.get('num_ratings', 0),
            stock=data.get('stock', 0),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        )
    
    def __repr__(self):
        return f"Product(id={self.product_id}, name={self.name}, category={self.category})"
