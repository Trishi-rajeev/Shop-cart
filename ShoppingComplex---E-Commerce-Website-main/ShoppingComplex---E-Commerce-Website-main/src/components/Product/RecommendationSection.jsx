import React, { useContext } from 'react';
import { ShopContext } from '../../context/ShopContext';
import ProductCard from './ProductCard';
import './RecommendationSection.css';

const RecommendationSection = () => {
    const { recommendations } = useContext(ShopContext);

    if (recommendations.length === 0) return null;

    return (
        <div className="recommendation-section">
            <h3>Recommended for You</h3>
            <div className="rec-grid">
                {recommendations.map(product => (
                    <ProductCard key={product.id} product={product} />
                ))}
            </div>
        </div>
    );
};

export default RecommendationSection;
