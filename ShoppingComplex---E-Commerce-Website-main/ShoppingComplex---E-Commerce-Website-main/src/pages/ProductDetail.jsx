import React, { useContext, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ShopContext } from '../context/ShopContext';
import SimilarProducts from '../components/Product/SimilarProducts';
import './ProductDetail.css';

const ProductDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const { products, addToCart, addToHistory, trackPurchase } = useContext(ShopContext);

    const product = products.find(p => p.id === parseInt(id));

    // Track product view when component mounts
    useEffect(() => {
        if (product) {
            addToHistory(product.id);
        }
    }, [product, addToHistory]);

    if (!product) {
        return (
            <div className="container" style={{ marginTop: '50px', textAlign: 'center' }}>
                <h2>Product not found</h2>
                <button onClick={() => navigate('/')} className="btn btn-primary">Go Back Home</button>
            </div>
        );
    }

    const handleBuyNow = () => {
        addToCart(product);
        // Track purchase in backend
        trackPurchase(product.id);
        alert('Product added to cart! Proceeding to checkout...');
        // In a real app, navigate to checkout page
    };

    const handleAddToCart = () => {
        addToCart(product);
        alert('Product added to cart successfully!');
    };

    return (
        <div className="product-detail-container">
            <div className="container">
                <button onClick={() => navigate(-1)} className="back-button">← Back</button>

                <div className="product-detail-content">
                    <div className="product-detail-image">
                        <img src={product.image} alt={product.name} />
                    </div>

                    <div className="product-detail-info">
                        <h1 className="product-detail-title">{product.name}</h1>
                        <p className="product-detail-category">{product.category}</p>

                        <div className="product-detail-price">₹ {product.price.toFixed(2)}</div>

                        <div className="product-detail-description">
                            <h3>Product Description</h3>
                            <p>
                                Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches)
                                in the padded sleeve, your everyday essentials in the main compartment, and small items in the
                                front zippered pocket. This versatile {product.category} item is designed for comfort and durability.
                            </p>
                        </div>

                        <div className="product-detail-meta">
                            <span>⭐ {product.rating} Rating</span>
                            <span>📦 {product.sold} sold</span>
                        </div>

                        <div className="product-detail-actions">
                            <button onClick={handleAddToCart} className="btn btn-outline-large">
                                Add to Cart
                            </button>
                            <button onClick={handleBuyNow} className="btn btn-primary-large">
                                Buy Now
                            </button>
                        </div>
                    </div>
                </div>

                {/* Similar Products Section */}
                <SimilarProducts productId={product.id} />
            </div>
        </div>
    );
};

export default ProductDetail;

