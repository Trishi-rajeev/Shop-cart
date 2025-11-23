import React from 'react';
import { Link } from 'react-router-dom';
import './HeroSection.css';

const HeroSection = () => {
    return (
        <div className="hero-section">
            <div className="hero-banner">
                <div className="banner-content">
                    <h2>Source factory-direct</h2>
                    <p>Quality products, wholesale prices</p>
                    <button className="btn btn-primary">View More</button>
                </div>
            </div>
            <div className="user-card">
                <div className="user-welcome">
                    <div className="avatar">👤</div>
                    <p>Hi, welcome to ShoppingComplex</p>
                </div>
                <div className="user-buttons">
                    <Link to="/login" className="btn btn-primary" style={{ width: '100%', textAlign: 'center' }}>Login</Link>
                    <Link to="/signup" className="btn btn-outline" style={{ width: '100%', textAlign: 'center' }}>Signup</Link>
                </div>
            </div>
        </div>
    );
};

export default HeroSection;
