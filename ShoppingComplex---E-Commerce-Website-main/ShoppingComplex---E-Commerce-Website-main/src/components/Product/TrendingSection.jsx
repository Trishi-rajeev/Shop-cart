import React, { useContext } from 'react';
import { ShopContext } from '../../context/ShopContext';
import ProductCard from './ProductCard';
import './TrendingSection.css';

const TrendingSection = () => {
    const { trendingProducts } = useContext(ShopContext);

    if (!trendingProducts || trendingProducts.length === 0) return null;

    return (
        <div className="trending-section">
            <div className="section-header">
                <h2>🔥 Trending Now</h2>
                <p>Most popular products this week</p>
            </div>
            <div className="trending-grid">
                {trendingProducts.map(product => (
                    <ProductCard key={product.id} product={product} />
                ))}
            </div>
        </div>
    );
};

export default TrendingSection;
