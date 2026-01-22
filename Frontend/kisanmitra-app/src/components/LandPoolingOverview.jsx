import React from 'react';
import {
    Users,
    TrendingUp,
    Truck,
    ArrowRight,
    Share2,
    Info
} from 'lucide-react';
import '../styles/global.css';

const LandPoolingOverview = ({ onJoinClick }) => {
    return (
        <div className="fade-in">
            {/* Header Section */}
            <div style={{ marginBottom: '32px', display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between' }}>
                <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', color: 'var(--color-primary-green)' }}>
                        <Users size={20} />
                        <span style={{ fontSize: '0.9rem', fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Collaborative Farming</span>
                    </div>
                    <h2 style={{ fontSize: '2rem', fontWeight: '900', margin: 0, color: 'var(--color-text-dark)' }}>Land Pooling Overview</h2>
                    <p style={{ fontSize: '1.1rem', color: 'var(--color-text-muted)', marginTop: '8px' }}>Unite resources for better yield and bargaining power.</p>
                </div>
                <button style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '8px 16px',
                    backgroundColor: 'white',
                    border: '1px solid var(--color-border)',
                    borderRadius: '8px',
                    fontWeight: '500',
                    color: 'var(--color-text-dark)'
                }}>
                    <Share2 size={18} /> Invite Farmers
                </button>
            </div>

            {/* Hero Stats Card */}
            <div className="card" style={{
                padding: '0',
                overflow: 'hidden',
                marginBottom: '24px',
                backgroundColor: 'var(--color-card-brown)',
                position: 'relative'
            }}>
                {/* Background Image / Gradient */}
                <div style={{
                    position: 'absolute',
                    top: 0,
                    right: 0,
                    width: '50%',
                    height: '100%',
                    backgroundImage: 'url(https://lh3.googleusercontent.com/aida-public/AB6AXuCIgywCIKe6wLzgbdS806KqL5B04fqsKRbfk9k0bRNSULWUYa29kP7plxJon9ejgrY1yDN-vaL-Gn7aiWCllQVhQ0eui_JrzA3DsNyXdGrHFpKxmps6PDoaQHocQIVwzCCJF8X-mx6djAmq4sEbUz5QOFflVhLs2FTILE9Y22YDRObIwVvMv_TlM14lfEYPoGgBgHNbV3KygeOuCSsbjkkppFQxkuqStgTGIZ7X2sk4I-oAP7cSprzwseD9JMiOErW91WApx5uU59Y)',
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    opacity: 0.2
                }}></div>
                <div style={{
                    position: 'absolute',
                    inset: 0,
                    background: 'linear-gradient(to right, var(--color-card-brown) 40%, transparent)'
                }}></div>

                {/* Content */}
                <div style={{ padding: '40px', position: 'relative', zIndex: 1 }}>
                    <h3 style={{ fontSize: '1.8rem', fontWeight: 'bold', marginBottom: '32px' }}>Collective Strength</h3>

                    <div style={{ display: 'flex', gap: '48px', marginBottom: '32px' }}>
                        <div style={{ display: 'flex', alignItems: 'start', gap: '16px' }}>
                            <div style={{
                                width: '56px',
                                height: '56px',
                                borderRadius: '12px',
                                backgroundColor: 'rgba(76, 175, 80, 0.2)',
                                color: 'var(--color-primary-green)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center'
                            }}>
                                <Users size={32} />
                            </div>
                            <div>
                                <p style={{ fontSize: '2.5rem', fontWeight: '900', margin: 0 }}>150</p>
                                <p style={{ fontSize: '1.1rem', fontWeight: 'bold', color: 'var(--color-text-muted)', margin: 0 }}>Acres Pooled</p>
                            </div>
                        </div>

                        <div style={{ width: '1px', backgroundColor: 'var(--color-border)' }}></div>

                        <div style={{ display: 'flex', alignItems: 'start', gap: '16px' }}>
                            <div style={{
                                width: '56px',
                                height: '56px',
                                borderRadius: '12px',
                                backgroundColor: 'rgba(217, 165, 76, 0.2)',
                                color: 'var(--color-accent-ochre)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center'
                            }}>
                                <Users size={32} />
                            </div>
                            <div>
                                <p style={{ fontSize: '2.5rem', fontWeight: '900', margin: 0 }}>12</p>
                                <p style={{ fontSize: '1.1rem', fontWeight: 'bold', color: 'var(--color-text-muted)', margin: 0 }}>Farmers Joined</p>
                            </div>
                        </div>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <div style={{ display: 'flex', marginLeft: '12px' }}>
                            {[1, 2, 3].map(i => (
                                <div key={i} style={{
                                    width: '40px',
                                    height: '40px',
                                    borderRadius: '50%',
                                    backgroundColor: '#ddd',
                                    border: '3px solid white',
                                    marginLeft: '-12px',
                                    backgroundImage: `url(https://placehold.co/100x100?text=${i})`,
                                    backgroundSize: 'cover'
                                }}></div>
                            ))}
                            <div style={{
                                width: '40px',
                                height: '40px',
                                borderRadius: '50%',
                                backgroundColor: 'var(--color-primary-green)',
                                border: '3px solid white',
                                marginLeft: '-12px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '0.8rem',
                                fontWeight: 'bold',
                                color: 'white'
                            }}>+9</div>
                        </div>
                        <span style={{ fontWeight: '500', color: 'var(--color-text-muted)' }}>Active in Village Rampur</span>
                    </div>
                </div>
            </div>

            {/* Benefits Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px', marginBottom: '24px' }}>
                <div className="card" style={{ backgroundColor: '#FBF5E6', border: '1px solid rgba(217, 165, 76, 0.2)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
                        <div style={{ padding: '12px', backgroundColor: 'white', borderRadius: '50%', color: 'var(--color-accent-ochre)' }}>
                            <Truck size={24} />
                        </div>
                        <span style={{ padding: '4px 12px', backgroundColor: 'rgba(255,255,255,0.6)', borderRadius: '20px', fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--color-accent-ochre)', height: 'fit-content' }}>LOGISTICS</span>
                    </div>
                    <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '8px' }}>20% Lower Transport Cost</h3>
                    <p style={{ color: 'var(--color-text-muted)', lineHeight: '1.6' }}>By pooling produce, we utilize full truckloads, significantly reducing per-unit transportation expenses to the city market.</p>
                </div>

                <div className="card" style={{ backgroundColor: '#E8F0E9', border: '1px solid rgba(76, 175, 80, 0.2)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
                        <div style={{ padding: '12px', backgroundColor: 'white', borderRadius: '50%', color: 'var(--color-primary-green)' }}>
                            <TrendingUp size={24} />
                        </div>
                        <span style={{ padding: '4px 12px', backgroundColor: 'rgba(255,255,255,0.6)', borderRadius: '20px', fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--color-primary-green)', height: 'fit-content' }}>MARKET ACCESS</span>
                    </div>
                    <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '8px' }}>Better Bulk Mandi Prices</h3>
                    <p style={{ color: 'var(--color-text-muted)', lineHeight: '1.6' }}>Aggregated volume gives us stronger negotiating power at the Mandi, ensuring premium rates for our collective harvest.</p>
                </div>
            </div>

            {/* Next Cycle CTA */}
            <div className="card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '24px', backgroundColor: 'white' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <div style={{ width: '48px', height: '48px', borderRadius: '50%', backgroundColor: 'var(--color-card-brown)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <Info size={24} />
                    </div>
                    <div>
                        <h4 style={{ fontSize: '1.1rem', fontWeight: 'bold', margin: 0 }}>Next Pooling Cycle</h4>
                        <p style={{ color: 'var(--color-text-muted)', margin: '4px 0 0 0' }}>Registration closes in 5 days for the Kharif season.</p>
                    </div>
                </div>
                <button
                    onClick={onJoinClick}
                    style={{
                        padding: '12px 32px',
                        backgroundColor: 'var(--color-primary-green)',
                        color: 'white',
                        fontSize: '1.1rem',
                        fontWeight: 'bold',
                        borderRadius: '12px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        boxShadow: '0 4px 12px rgba(76, 175, 80, 0.2)'
                    }}
                >
                    Join the Pool <ArrowRight size={20} />
                </button>
            </div>
        </div>
    );
};

export default LandPoolingOverview;
