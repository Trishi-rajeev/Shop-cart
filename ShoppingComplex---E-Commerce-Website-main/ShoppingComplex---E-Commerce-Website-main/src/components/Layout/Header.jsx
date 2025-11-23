import React, { useContext, useState } from 'react';
import { Link } from 'react-router-dom';
import { ShopContext } from '../../context/ShopContext';
import './Header.css';

const Header = () => {
    const { cart } = useContext(ShopContext);
    const [menuOpen, setMenuOpen] = useState(false);

    return (
        <header className="header">
            <div className="top-bar">
                <div className="container top-bar-content">
                    <span>Sourcing solutions services & membership help & community</span>
                    <div className="top-links">
                        <span>ShoppingComplex</span>
                        <span>Orders</span>
                        <span>Cart ({cart.length})</span>
                    </div>
                </div>
            </div>
            <div className="main-header container">
                <div className="logo">
                    <h1 style={{ color: 'var(--primary-orange)', fontStyle: 'italic' }}>ShoppingComplex</h1>
                </div>
                <div className="search-bar">
                    <div className="search-input-group">
                        <select className="search-select">
                            <option>Products</option>
                            <option>Suppliers</option>
                        </select>
                        <input type="text" placeholder="What are you looking for..." />
                        <button className="search-btn">Search</button>
                    </div>
                </div>
                <div className="user-actions">
                    <div className="action-item">
                        <span className="icon">👤</span>
                        <div className="text">
                            <Link to="/login" style={{ fontSize: '12px', color: 'var(--text-light)' }}>Login</Link>
                            <Link to="/signup" style={{ fontWeight: 'bold', color: 'var(--text-dark)' }}>Signup</Link>
                        </div>
                    </div>
                    <div className="action-item">
                        <span className="icon">💬</span>
                        <div className="text">
                            <small>Messages</small>
                        </div>
                    </div>
                </div>

                {/* Hamburger Menu Button - Right Side */}
                <button
                    className={`hamburger-menu ${menuOpen ? 'open' : ''}`}
                    onClick={() => setMenuOpen(!menuOpen)}
                    aria-label="Toggle menu"
                >
                    <span></span>
                    <span></span>
                    <span></span>
                </button>
            </div>

            {/* Mobile Menu Dropdown */}
            {menuOpen && (
                <div className="mobile-menu">
                    <div className="mobile-menu-item">
                        <div className="search-bar-mobile">
                            <input type="text" placeholder="Search products..." />
                            <button className="search-btn">🔍</button>
                        </div>
                    </div>
                    <Link to="/login" className="mobile-menu-item" onClick={() => setMenuOpen(false)}>
                        <span className="icon">👤</span>
                        <span>Login</span>
                    </Link>
                    <Link to="/signup" className="mobile-menu-item" onClick={() => setMenuOpen(false)}>
                        <span className="icon">✍️</span>
                        <span>Signup</span>
                    </Link>
                    <div className="mobile-menu-item">
                        <span className="icon">💬</span>
                        <span>Messages</span>
                    </div>
                </div>
            )}
        </header>
    );
};

export default Header;
