import React, { useState, useEffect, useContext } from 'react';
import PropTypes from 'prop-types';
import { ShopContext } from '../../context/ShopContext';
import ProductCard from './ProductCard';
import './SimilarProducts.css';

const SimilarProducts = ({ productId }) => {
    const { getSimilarProductsForItem, backendConnected } = useContext(ShopContext);
    const [similarProducts, setSimilarProducts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        console.log('SimilarProducts: Starting fetch for productId:', productId);

        if (!productId || !getSimilarProductsForItem) {
            console.log('SimilarProducts: Missing productId or getSimilarProductsForItem');
            setLoading(false);
            return;
        }

        setLoading(true);

        try {
            // Call the function directly (it's synchronous, not async)
            const similar = getSimilarProductsForItem(productId, 6);
            console.log('SimilarProducts: Received similar products:', similar);
            setSimilarProducts(similar || []);
        } catch (error) {
            console.error('SimilarProducts: Error fetching similar products:', error);
            setSimilarProducts([]);
        } finally {
            console.log('SimilarProducts: Setting loading to false');
            setLoading(false);
        }
    }, [productId, getSimilarProductsForItem]);

    if (loading) {
        return (
            <div className="similar-products-section">
                <h3>Similar Products</h3>
                <div className="loading-spinner">Loading...</div>
            </div>
        );
    }

    if (!similarProducts || similarProducts.length === 0) {
        return (
            <div className="similar-products-section">
                <h3>You May Also Like</h3>
                <p style={{ textAlign: 'center', color: '#666', padding: '20px' }}>
                    {backendConnected
                        ? 'No similar products found at the moment.'
                        : 'Browse our catalog to discover more products!'}
                </p>
            </div>
        );
    }

    return (
        <div className="similar-products-section">
            <h3>You May Also Like</h3>
            <div className="similar-grid">
                {similarProducts.map(product => (
                    <ProductCard key={product.id} product={product} />
                ))}
            </div>
        </div>
    );
};

SimilarProducts.propTypes = {
    productId: PropTypes.number.isRequired
};

export default SimilarProducts;

