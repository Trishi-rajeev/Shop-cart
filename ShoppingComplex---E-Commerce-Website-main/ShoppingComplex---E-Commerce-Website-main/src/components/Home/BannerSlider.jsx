import React, { useState, useEffect } from 'react';
import './BannerSlider.css';

const BannerSlider = () => {
    const [currentSlide, setCurrentSlide] = useState(0);

    const slides = [
        {
            id: 1,
            title: 'Office Chairs',
            subtitle: 'From ₹2,999',
            description: 'Green Soul, Cell Bell & more',
            bgColor: '#2874f0',
            image: 'https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=400'
        },
        {
            id: 2,
            title: 'Electronics Sale',
            subtitle: 'Up to 70% OFF',
            description: 'Laptops, Mobiles & Accessories',
            bgColor: '#ff6b6b',
            image: 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400'
        },
        {
            id: 3,
            title: 'Fashion Trends',
            subtitle: 'Starting ₹199',
            description: 'Clothing, Footwear & More',
            bgColor: '#4ecdc4',
            image: 'https://images.unsplash.com/photo-1445205170230-053b83016050?w=400'
        },
        {
            id: 4,
            title: 'Home Decor',
            subtitle: 'Min 50% OFF',
            description: 'Furniture, Kitchen & More',
            bgColor: '#f39c12',
            image: 'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=400'
        }
    ];

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentSlide((prev) => (prev + 1) % slides.length);
        }, 3000); // Auto-slide every 3 seconds

        return () => clearInterval(timer);
    }, [slides.length]);

    const goToSlide = (index) => {
        setCurrentSlide(index);
    };

    const nextSlide = () => {
        setCurrentSlide((prev) => (prev + 1) % slides.length);
    };

    const prevSlide = () => {
        setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
    };

    return (
        <div className="banner-slider">
            <div className="slider-container">
                <button className="slider-arrow slider-arrow-left" onClick={prevSlide}>
                    ‹
                </button>

                <div className="slides-wrapper">
                    {slides.map((slide, index) => (
                        <div
                            key={slide.id}
                            className={`slide ${index === currentSlide ? 'active' : ''}`}
                            style={{ backgroundColor: slide.bgColor }}
                        >
                            <div className="slide-content">
                                <div className="slide-text">
                                    <h2>{slide.title}</h2>
                                    <h3>{slide.subtitle}</h3>
                                    <p>{slide.description}</p>
                                    <button className="shop-now-btn">Shop Now</button>
                                </div>
                                <div className="slide-image">
                                    <img src={slide.image} alt={slide.title} />
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <button className="slider-arrow slider-arrow-right" onClick={nextSlide}>
                    ›
                </button>
            </div>

            <div className="slider-dots">
                {slides.map((_, index) => (
                    <button
                        key={index}
                        className={`dot ${index === currentSlide ? 'active' : ''}`}
                        onClick={() => goToSlide(index)}
                    />
                ))}
            </div>
        </div>
    );
};

export default BannerSlider;
