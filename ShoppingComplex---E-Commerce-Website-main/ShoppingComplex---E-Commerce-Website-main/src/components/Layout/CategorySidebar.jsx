import React from 'react';
import { categories } from '../../data/mockData';
import './CategorySidebar.css';

const CategorySidebar = () => {
    return (
        <div className="category-sidebar">
            <h3>My Markets</h3>
            <ul>
                {categories.map(cat => (
                    <li key={cat.id} className="category-item">
                        <span className="cat-icon"></span>
                        <span className="cat-name">{cat.name}</span>
                        <div className="sub-menu">
                            {cat.sub.map(s => (
                                <div key={s} className="sub-item">{s}</div>
                            ))}
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CategorySidebar;
