# E-Commerce Recommendation System Backend

A comprehensive Python-based recommendation system for e-commerce applications, featuring collaborative filtering, content-based filtering, and hybrid approaches.

## Features

### Recommendation Algorithms
- **Collaborative Filtering**: User-based and item-based recommendations using cosine similarity
- **Content-Based Filtering**: TF-IDF vectorization of product features for similarity matching
- **Hybrid Recommender**: Combines both approaches with configurable weights
- **Trending Products**: Time-based trending analysis with weighted interactions

### API Capabilities
- Personalized user recommendations
- Similar product recommendations
- Trending products
- Product filtering by price, rating, and category
- User interaction tracking (views, purchases, cart, wishlist, ratings)
- Real-time model retraining
- Response caching for improved performance

## Project Structure

```
Backend/
├── app.py                          # Flask REST API
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
│
├── models/                         # Data models
│   ├── __init__.py
│   ├── product.py                  # Product model
│   ├── user.py                     # User model
│   └── interaction.py              # User-product interaction model
│
├── recommender/                    # Recommendation algorithms
│   ├── __init__.py
│   ├── collaborative_filtering.py  # Collaborative filtering
│   ├── content_based.py            # Content-based filtering
│   └── hybrid_recommender.py       # Hybrid approach
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   └── data_utils.py               # Data management and processing
│
└── data/                           # Sample data
    ├── products.json               # Product catalog
    ├── users.json                  # User profiles
    └── interactions.json           # User-product interactions
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Navigate to the Backend directory**
   ```bash
   cd Backend
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example environment file
   copy .env.example .env
   
   # Edit .env with your settings
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```
Returns system status and data counts.

### User Recommendations
```
GET /api/recommendations/user/<user_id>
```
Get personalized recommendations for a specific user.

**Query Parameters:**
- `n` (int): Number of recommendations (default: 10)
- `min_price` (float): Minimum price filter
- `max_price` (float): Maximum price filter
- `min_rating` (float): Minimum rating filter
- `diversity` (bool): Enable diversity re-ranking

**Example:**
```bash
curl "http://localhost:5000/api/recommendations/user/user001?n=5&min_rating=4.0"
```

### Similar Products
```
GET /api/recommendations/similar/<product_id>
```
Get products similar to a given product.

**Query Parameters:**
- `n` (int): Number of recommendations (default: 10)
- `method` (string): 'collaborative', 'content', or 'hybrid' (default: hybrid)

**Example:**
```bash
curl "http://localhost:5000/api/recommendations/similar/prod001?n=5&method=hybrid"
```

### Trending Products
```
GET /api/recommendations/trending
```
Get currently trending products.

**Query Parameters:**
- `n` (int): Number of recommendations (default: 10)
- `days` (int): Time window in days (default: 7)

**Example:**
```bash
curl "http://localhost:5000/api/recommendations/trending?n=10&days=7"
```

### Add Interaction
```
POST /api/interactions
```
Track a user-product interaction.

**Request Body:**
```json
{
  "user_id": "user001",
  "product_id": "prod001",
  "interaction_type": "purchase",
  "rating": 5.0
}
```

**Interaction Types:**
- `view`: User viewed the product
- `cart`: User added to cart
- `purchase`: User purchased the product
- `rating`: User rated the product
- `wishlist`: User added to wishlist

### Get Products
```
GET /api/products
```
Get all products with optional filtering.

**Query Parameters:**
- `category` (string): Filter by category
- `min_price` (float): Minimum price
- `max_price` (float): Maximum price
- `min_rating` (float): Minimum rating

### Retrain Model
```
POST /api/retrain
```
Manually trigger model retraining with current data.

## Configuration

Edit the `.env` file to customize settings:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
DEBUG=True

# Recommendation Settings
MIN_RATINGS=5
MAX_RECOMMENDATIONS=10
SIMILARITY_THRESHOLD=0.3

# Model Weights (must sum to 1.0)
COLLABORATIVE_WEIGHT=0.6
CONTENT_WEIGHT=0.4

# Cache Settings
CACHE_ENABLED=True
CACHE_TTL=3600

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Usage Examples

### Python Client Example

```python
import requests

# Get user recommendations
response = requests.get(
    'http://localhost:5000/api/recommendations/user/user001',
    params={'n': 5, 'min_rating': 4.0}
)
recommendations = response.json()

# Track a purchase
requests.post(
    'http://localhost:5000/api/interactions',
    json={
        'user_id': 'user001',
        'product_id': 'prod005',
        'interaction_type': 'purchase',
        'rating': 5.0
    }
)

# Get similar products
response = requests.get(
    'http://localhost:5000/api/recommendations/similar/prod001',
    params={'n': 5, 'method': 'hybrid'}
)
similar = response.json()
```

### JavaScript/React Example

```javascript
// Get user recommendations
const getUserRecommendations = async (userId) => {
  const response = await fetch(
    `http://localhost:5000/api/recommendations/user/${userId}?n=10`
  );
  const data = await response.json();
  return data.recommendations;
};

// Track interaction
const trackInteraction = async (userId, productId, type) => {
  await fetch('http://localhost:5000/api/interactions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      product_id: productId,
      interaction_type: type
    })
  });
};
```

## Algorithm Details

### Collaborative Filtering
- Uses user-item interaction matrix
- Calculates user and item similarity using cosine similarity
- Supports both user-based and item-based approaches
- Weights different interaction types (purchase > cart > wishlist > view)

### Content-Based Filtering
- Uses TF-IDF vectorization of product features
- Combines product name, category, brand, description, and tags
- Creates user profiles from interaction history
- Recommends products similar to user preferences

### Hybrid Approach
- Combines collaborative and content-based scores
- Configurable weights for each method
- Provides more robust recommendations
- Handles cold-start problems better

## Performance Optimization

- **Caching**: Responses are cached with configurable TTL
- **Batch Processing**: Model retraining happens periodically
- **Efficient Algorithms**: Uses NumPy and scikit-learn for fast computations
- **Lazy Loading**: Models are loaded on demand

## Production Deployment

For production deployment:

1. **Use a proper database** (PostgreSQL, MongoDB)
2. **Set up Redis** for caching
3. **Use Gunicorn** or uWSGI as WSGI server
4. **Enable HTTPS** with SSL certificates
5. **Set up monitoring** and logging
6. **Use environment-specific configs**
7. **Implement rate limiting**
8. **Add authentication** for API endpoints

Example production startup:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Testing

The system includes sample data for testing:
- 10 sample products across different categories
- 3 sample users with preferences
- 10 sample interactions

You can test the API immediately after installation using the provided sample data.

## Extending the System

### Adding New Recommendation Algorithms

Create a new file in `recommender/` directory:

```python
class NewRecommender:
    def fit(self, data):
        # Train your model
        pass
    
    def recommend(self, user_id, n=10):
        # Generate recommendations
        pass
```

### Adding New Data Sources

Modify `app.py` to load data from your database:

```python
def load_data():
    # Load from database instead of JSON files
    products_data = db.query(Product).all()
    interactions_data = db.query(Interaction).all()
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Port already in use**: Change the port in `.env` file
   ```env
   API_PORT=5001
   ```

3. **CORS errors**: Add your frontend URL to CORS_ORIGINS
   ```env
   CORS_ORIGINS=http://localhost:3000
   ```

## License

This project is open source and available for use in your e-commerce applications.

## Support

For issues or questions, please refer to the code documentation or create an issue in the project repository.
