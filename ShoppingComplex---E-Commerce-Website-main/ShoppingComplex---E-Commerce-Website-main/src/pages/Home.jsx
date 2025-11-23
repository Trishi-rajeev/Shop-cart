import React, { useContext } from 'react';
import { ShopContext } from '../context/ShopContext';
import BannerSlider from '../components/Home/BannerSlider';
import CategorySidebar from '../components/Layout/CategorySidebar';
import HeroSection from '../components/Home/HeroSection';
import RecommendationSection from '../components/Product/RecommendationSection';
import TrendingSection from '../components/Product/TrendingSection';
import ProductCard from '../components/Product/ProductCard';

const Home = () => {
    const { products } = useContext(ShopContext);

    return (
        <div className="container" style={{ marginTop: '20px' }}>
            <BannerSlider />

            <div style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
                <CategorySidebar />
                <div style={{ flex: 1 }}>
                    <HeroSection />
                </div>
            </div>

            {/* Trending Products Section */}
            <TrendingSection />

            <div style={{ marginTop: '40px' }}>
                <h3 style={{ fontSize: '20px', marginBottom: '20px' }}>Just For You</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '16px' }}>
                    {products.map(p => (
                        <ProductCard key={p.id} product={p} />
                    ))}
                </div>
            </div>

            {/* Personalized Recommendations */}
            <RecommendationSection />
        </div>
    );
};

export default Home;

