# Backend Integration Guide

## Quick Start

### 1. Start the Python Backend

```bash
cd Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend will run on `http://localhost:5000`

### 2. Start the React Frontend

```bash
# In the main project directory
npm run dev
```

Frontend will run on `http://localhost:5173`

## Environment Configuration

The `.env` file has been created with:
- `VITE_API_URL=http://localhost:5000`
- `VITE_DEFAULT_USER_ID=user001`

## Features Integrated

### ✅ Automatic Interaction Tracking
- **Product Views**: Tracked when user visits product detail page
- **Add to Cart**: Tracked when user adds product to cart
- **Purchases**: Tracked when user clicks "Buy Now"

### ✅ Recommendation Components
- **User Recommendations**: Personalized recommendations on homepage
- **Trending Products**: Shows trending items with gradient background
- **Similar Products**: Displays on product detail pages

### ✅ Fallback Support
- Works offline with local recommendation logic
- Automatically switches to backend when available
- `backendConnected` status available in ShopContext

## Testing the Integration

1. **Start both servers** (Backend and Frontend)
2. **Browse products** - Views are tracked automatically
3. **Add items to cart** - Cart actions are tracked
4. **Check recommendations** - Should update based on your activity
5. **View product details** - See similar products section

## API Endpoints Being Used

- `GET /api/recommendations/user/{userId}` - User recommendations
- `GET /api/recommendations/similar/{productId}` - Similar products
- `GET /api/recommendations/trending` - Trending products
- `POST /api/interactions` - Track user interactions

## Troubleshooting

**Backend not connecting?**
- Check if Python backend is running on port 5000
- Verify CORS settings in Backend/.env
- Check browser console for errors

**No recommendations showing?**
- Backend needs sample data to work
- Interact with products to generate data
- Check Backend/data/ folder for sample data

**CORS errors?**
- Update Backend/.env CORS_ORIGINS to include your frontend URL
- Restart the Python backend after changes
