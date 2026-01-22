import React, { useState } from 'react';
import { ArrowLeft, TrendingUp, Truck, MapPin, DollarSign, Clock, Leaf, Recycle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import '../styles/global.css';

const PostHarvestStage = () => {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('market'); // market | residuals
    const [analysisDone, setAnalysisDone] = useState(false);

    return (
        <div style={{ paddingBottom: '80px' }}>
            {/* Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
                <button
                    onClick={() => navigate('/farm-management')}
                    style={{ background: 'none', padding: '4px' }}
                >
                    <ArrowLeft size={24} color="var(--color-text-dark)" />
                </button>
                <h2 style={{ fontSize: '1.25rem', margin: 0 }}>Post-Harvest</h2>
            </div>

            {/* Tabs */}
            <div style={{
                display: 'flex',
                gap: '12px',
                marginBottom: '24px',
                borderBottom: '1px solid var(--color-border)',
                paddingBottom: '12px'
            }}>
                <button
                    onClick={() => setActiveTab('market')}
                    style={{
                        flex: 1,
                        padding: '12px',
                        borderRadius: '8px',
                        backgroundColor: activeTab === 'market' ? 'var(--color-primary-green)' : 'transparent',
                        color: activeTab === 'market' ? 'white' : 'var(--color-text-muted)',
                        fontWeight: '600',
                        textAlign: 'center'
                    }}
                >
                    Market & Selling
                </button>
                <button
                    onClick={() => setActiveTab('residuals')}
                    style={{
                        flex: 1,
                        padding: '12px',
                        borderRadius: '8px',
                        backgroundColor: activeTab === 'residuals' ? 'var(--color-primary-green)' : 'transparent',
                        color: activeTab === 'residuals' ? 'white' : 'var(--color-text-muted)',
                        fontWeight: '600',
                        textAlign: 'center'
                    }}
                >
                    Stubbles (Parali)
                </button>
            </div>

            {/* Market Section */}
            {activeTab === 'market' && (
                !analysisDone ? (
                    <div className="card">
                        <h3 style={{ marginBottom: '16px' }}>Check Best Price</h3>

                        <div style={{ marginBottom: '16px' }}>
                            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Crop Harvested</label>
                            <select style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid #ccc', fontSize: '1rem', backgroundColor: 'white' }}>
                                <option>Wheat (Lokwan)</option>
                                <option>Rice (Basmati)</option>
                                <option>Soybean</option>
                            </select>
                        </div>

                        <div style={{ marginBottom: '24px' }}>
                            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Quantity (Quintals)</label>
                            <input type="number" placeholder="e.g. 50" style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid #ccc', fontSize: '1rem' }} />
                        </div>

                        <button
                            onClick={() => setAnalysisDone(true)}
                            style={{ width: '100%', padding: '14px', backgroundColor: 'var(--color-primary-green)', color: 'white', borderRadius: '8px', fontWeight: 'bold' }}
                        >
                            Analyze Market
                        </button>
                    </div>
                ) : (
                    <div>
                        <div style={{
                            backgroundColor: '#E3F2FD',
                            padding: '16px',
                            borderRadius: '12px',
                            marginBottom: '24px',
                            border: '1px solid #90CAF9'
                        }}>
                            <h3 style={{ margin: '0 0 8px 0', fontSize: '1.1rem', color: '#1565C0', display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <Clock size={20} /> Recommendation: HOLD
                            </h3>
                            <p style={{ margin: 0, color: '#0D47A1', fontSize: '0.95rem' }}>
                                Prices are rising. Hold for <strong>15 days</strong> to earn approx <strong>₹12,000 more</strong>.
                            </p>
                        </div>

                        <h4 style={{ marginBottom: '12px', color: 'var(--color-text-muted)' }}>Selling Options</h4>

                        {/* Option 1: Sell Now */}
                        <div className="card" style={{ marginBottom: '16px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                                <div style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>Mandsaur Mandi</div>
                                <div style={{ padding: '4px 8px', backgroundColor: '#FFF3E0', color: '#E65100', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold' }}>SELL NOW</div>
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', fontSize: '0.9rem', marginBottom: '12px' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--color-text-muted)' }}>
                                    <MapPin size={16} /> 12 km
                                </div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--color-text-muted)' }}>
                                    <Truck size={16} /> ₹400 Transport
                                </div>
                            </div>

                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--color-border)', paddingTop: '12px' }}>
                                <div>
                                    <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>Net Price</div>
                                    <div style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>₹2,150 / qt</div>
                                </div>
                                <button style={{ padding: '8px 16px', border: '1px solid var(--color-primary-green)', backgroundColor: 'white', color: 'var(--color-primary-green)', borderRadius: '6px', fontWeight: '600' }}>
                                    Sell Here
                                </button>
                            </div>
                        </div>

                        {/* Option 2: Hold */}
                        <div className="card" style={{ border: '2px solid var(--color-primary-green)' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
                                <div style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>Wait 15 Days</div>
                                <div style={{ padding: '4px 8px', backgroundColor: '#E8F5E9', color: '#1B5E20', borderRadius: '4px', fontSize: '0.8rem', fontWeight: 'bold' }}>BEST CHOICE</div>
                            </div>

                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                                <TrendingUp size={20} color="var(--color-primary-green)" />
                                <span style={{ fontSize: '0.9rem' }}>Market trend is bullish (+8%)</span>
                            </div>

                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--color-border)', paddingTop: '12px' }}>
                                <div>
                                    <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>Predicted Price</div>
                                    <div style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>₹2,320 / qt</div>
                                </div>
                                <button style={{ padding: '8px 16px', backgroundColor: 'var(--color-primary-green)', color: 'white', borderRadius: '6px', fontWeight: '600' }}>
                                    Choose to Hold
                                </button>
                            </div>
                        </div>

                        <button
                            onClick={() => setAnalysisDone(false)}
                            style={{ display: 'block', margin: '24px auto', color: 'var(--color-text-muted)', background: 'none', textDecoration: 'underline' }}
                        >
                            Analyze Another Crop
                        </button>
                    </div>
                )
            )}

            {/* Residuals Section */}
            {activeTab === 'residuals' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div className="card">
                        <h3 style={{ marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <Recycle color="var(--color-primary-green)" /> Wheat Straw (Bhusa)
                        </h3>
                        <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', marginBottom: '16px' }}>
                            Do not burn. You have 2 profitable options.
                        </p>

                        <div style={{
                            border: '1px solid var(--color-border)',
                            borderRadius: '8px',
                            padding: '12px',
                            marginBottom: '12px'
                        }}>
                            <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>Sell to Bio-fuel Plant</div>
                            <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', marginBottom: '8px' }}>
                                NTPC Plant is buying stubble. Pickup is free.
                            </p>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <span style={{ fontWeight: 'bold', color: 'var(--color-primary-green)' }}>Earn ₹2,000 / acre</span>
                                <button style={{ padding: '6px 12px', backgroundColor: 'var(--color-primary-green)', color: 'white', borderRadius: '4px', fontSize: '0.9rem' }}>Contact</button>
                            </div>
                        </div>

                        <div style={{
                            border: '1px solid var(--color-border)',
                            borderRadius: '8px',
                            padding: '12px'
                        }}>
                            <div style={{ fontWeight: 'bold', marginBottom: '4px' }}>Use for Mulching</div>
                            <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', marginBottom: '8px' }}>
                                Mix in soil to improve fertility for next crop.
                            </p>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <span style={{ fontWeight: 'bold', color: '#EF6C00' }}>Save ₹1,500 fertilizer</span>
                                <button style={{ padding: '6px 12px', backgroundColor: 'var(--color-bg-beige)', color: 'var(--color-text-dark)', borderRadius: '4px', fontSize: '0.9rem' }}>View Guide</button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PostHarvestStage;
