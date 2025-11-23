import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../index.css'; // Ensure global styles are available

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        // Mock login logic
        console.log('Login with:', email, password);
        // In a real app, you'd validate and store token
        navigate('/');
    };

    return (
        <div className="auth-container" style={{ maxWidth: '400px', margin: '100px auto', padding: '20px', background: '#fff', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
            <h2 style={{ textAlign: 'center', marginBottom: '20px', color: 'var(--primary-orange)' }}>Login</h2>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                <div>
                    <label style={{ display: 'block', marginBottom: '5px', fontSize: '14px' }}>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        style={{ width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '4px' }}
                    />
                </div>
                <div>
                    <label style={{ display: 'block', marginBottom: '5px', fontSize: '14px' }}>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={{ width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '4px' }}
                    />
                </div>
                <button type="submit" className="btn btn-primary" style={{ marginTop: '10px', width: '100%' }}>Login</button>
            </form>
            <p style={{ marginTop: '15px', textAlign: 'center', fontSize: '14px' }}>
                New here? <Link to="/signup" style={{ color: 'var(--primary-orange)', fontWeight: 'bold' }}>Signup</Link>
            </p>
        </div>
    );
};

export default Login;
