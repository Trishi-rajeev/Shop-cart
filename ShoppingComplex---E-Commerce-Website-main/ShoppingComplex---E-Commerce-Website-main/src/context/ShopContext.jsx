import React, { createContext, useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { products as mockProducts } from '../data/mockData'; // Keeping for fallback if needed, or just remove usage

export const ShopContext = createContext();

export const ShopProvider = ({ children }) => {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [viewHistory, setViewHistory] = useState([]);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    const fetchAllProducts = async () => {
      try {
        // Fetch from Fake Store API
        const fakeStoreResponse = await fetch('https://fakestoreapi.com/products');
        const fakeStoreData = await fakeStoreResponse.json();

        // Fetch from DummyJSON API
        const dummyJsonResponse = await fetch('https://dummyjson.com/products?limit=50');
        const dummyJsonData = await dummyJsonResponse.json();

        // Custom Indian products
        const customProducts = [
          {
            id: 1001,
            title: 'Samsung Galaxy S23 Ultra 5G',
            price: 89999,
            category: 'smartphones',
            image: 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400',
            rating: { rate: 4.7, count: 1250 }
          },
          {
            id: 1002,
            title: 'LG 55" 4K Smart TV',
            price: 45999,
            category: 'electronics',
            image: 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=400',
            rating: { rate: 4.5, count: 890 }
          },
          {
            id: 1003,
            title: 'Whirlpool 265L Refrigerator',
            price: 24999,
            category: 'appliances',
            image: 'https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5?w=400',
            rating: { rate: 4.3, count: 567 }
          },
          {
            id: 1004,
            title: 'Philips LED Smart Bulb',
            price: 599,
            category: 'lighting',
            image: 'https://images.unsplash.com/photo-1550985616-10810253b84d?w=400',
            rating: { rate: 4.2, count: 2340 }
          },
          {
            id: 1005,
            title: 'Milton Thermosteel Water Bottle 1L',
            price: 799,
            category: 'home & kitchen',
            image: 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400',
            rating: { rate: 4.6, count: 3450 }
          },
          {
            id: 1006,
            title: 'Prestige Induction Cooktop',
            price: 2499,
            category: 'appliances',
            image: 'https://images.unsplash.com/photo-1585659722983-3a675dabf23d?w=400',
            rating: { rate: 4.4, count: 1890 }
          },
          {
            id: 1007,
            title: 'Seiko Wall Clock',
            price: 1299,
            category: 'home decor',
            image: 'https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=400',
            rating: { rate: 4.5, count: 890 }
          },
          {
            id: 1008,
            title: 'Wooden Photo Frame Set of 3',
            price: 899,
            category: 'home decor',
            image: 'https://images.unsplash.com/photo-1513519245088-0e12902e35ca?w=400',
            rating: { rate: 4.3, count: 670 }
          },
          {
            id: 1009,
            title: 'Ceramic Water Jug with Glasses',
            price: 1499,
            category: 'home & kitchen',
            image: 'https://images.unsplash.com/photo-1584627904-1bc1c0c3c7d9?w=400',
            rating: { rate: 4.4, count: 450 }
          },
          {
            id: 1010,
            title: 'Bajaj Table Fan 400mm',
            price: 1899,
            category: 'appliances',
            image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400',
            rating: { rate: 4.2, count: 1200 }
          }
        ];

        // Combine all products
        const allProducts = [...fakeStoreData, ...dummyJsonData.products, ...customProducts];

        // Find max price
        const maxOriginalPrice = Math.max(...allProducts.map(item => item.price));

        // Adapt all products to uniform format
        const adaptedProducts = allProducts.map((item, index) => ({
          id: item.id || (2000 + index),
          name: item.title,
          // Normalize price from 200 to 50000
          price: 200 + ((item.price / maxOriginalPrice) * (50000 - 200)),
          category: item.category,
          image: item.image || item.thumbnail || 'https://via.placeholder.com/400',
          rating: item.rating?.rate || item.rating || 4.0,
          sold: item.rating?.count || item.stock || Math.floor(Math.random() * 1000)
        }));

        setProducts(adaptedProducts);
      } catch (err) {
        console.error("Failed to fetch products:", err);
      }
    };

    fetchAllProducts();
  }, []);

  // Simple recommendation logic: suggest products from categories user has viewed
  useEffect(() => {
    if (products.length === 0) return;

    if (viewHistory.length > 0) {
      const viewedCategories = new Set(viewHistory.map(id => {
        const p = products.find(prod => prod.id === id);
        return p ? p.category : null;
      }).filter(Boolean));

      const recs = products.filter(p => viewedCategories.has(p.category) && !viewHistory.includes(p.id));
      // If not enough recs, fill with random popular items
      if (recs.length < 5) {
        const others = products.filter(p => !viewHistory.includes(p.id) && !recs.includes(p));
        recs.push(...others.slice(0, 5 - recs.length));
      }
      setRecommendations(recs.slice(0, 10));
    } else {
      // Default recommendations
      setRecommendations(products.slice(0, 5));
    }
  }, [viewHistory, products]);

  const addToCart = (product) => {
    setCart(prev => [...prev, product]);
  };

  const addToHistory = (productId) => {
    setViewHistory(prev => {
      // Keep last 10 items
      const newHistory = [productId, ...prev.filter(id => id !== productId)];
      return newHistory.slice(0, 10);
    });
  };

  const getSimilarProductsForItem = (productId, n = 6) => {
    console.log('Getting similar products for product ID:', productId);
    const product = products.find(p => p.id === productId);

    if (!product) {
      console.log('Product not found');
      return [];
    }

    const similar = products
      .filter(p => p.category === product.category && p.id !== productId)
      .slice(0, n);

    console.log(`Found ${similar.length} similar products in category: ${product.category}`);
    return similar;
  };

  return (
    <ShopContext.Provider value={{
      products,
      cart,
      addToCart,
      recommendations,
      addToHistory,
      getSimilarProductsForItem
    }}>
      {children}
    </ShopContext.Provider>
  );
};

ShopProvider.propTypes = {
  children: PropTypes.node.isRequired,
};
