import React from 'react';
import {
    ChevronRight,
    Home,
    MapPin,
    Users,
    Calendar,
    Mic,
    FileText,
    Download,
    Check
} from 'lucide-react';
import '../styles/global.css';
import MapComponent from './MapComponent';

const LandPoolDetails = ({ pool, onBack, onJoin }) => {
    return (
        <div className="fade-in">
            {/* Breadcrumb */}
            <nav style={{ marginBottom: '24px', display: 'flex', alignItems: 'center', fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>
                <span style={{ cursor: 'pointer' }} onClick={onBack}>Land Pools</span>
                <ChevronRight size={16} />
                <span style={{ color: 'var(--color-primary-green)', fontWeight: '500' }}>Group Details</span>
            </nav>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '32px' }}>
                {/* Left Column: Details */}
                <div style={{ minWidth: '60%' }}>

                    {/* Header Info */}
                    <div style={{ marginBottom: '24px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                            <span style={{
                                padding: '4px 12px',
                                backgroundColor: 'rgba(217, 165, 76, 0.1)',
                                color: 'var(--color-accent-ochre)',
                                border: '1px solid rgba(217, 165, 76, 0.2)',
                                borderRadius: '16px',
                                fontSize: '0.75rem',
                                fontWeight: 'bold',
                                textTransform: 'uppercase'
                            }}>
                                Open for Pooling
                            </span>
                            <span style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>
                                <MapPin size={16} /> {pool.location || 'Ludhiana, Punjab'}
                            </span>
                        </div>
                        <h2 style={{ fontSize: '2.5rem', fontWeight: '900', margin: '0 0 12px 0', color: 'var(--color-text-dark)' }}>{pool.name || 'Unity Wheat Collective'}</h2>
                        <p style={{ fontSize: '1.1rem', color: 'var(--color-text-muted)', lineHeight: '1.6' }}>
                            A collaborative initiative for small-holder farmers to share mechanized harvesting resources and optimize market selling windows.
                        </p>
                    </div>

                    {/* Hero Image */}
                    <div style={{
                        height: '320px',
                        borderRadius: '16px',
                        overflow: 'hidden',
                        marginBottom: '24px',
                        position: 'relative'
                    }}>
                        <img
                            src="https://lh3.googleusercontent.com/aida-public/AB6AXuCIgywCIKe6wLzgbdS806KqL5B04fqsKRbfk9k0bRNSULWUYa29kP7plxJon9ejgrY1yDN-vaL-Gn7aiWCllQVhQ0eui_JrzA3DsNyXdGrHFpKxmps6PDoaQHocQIVwzCCJF8X-mx6djAmq4sEbUz5QOFflVhLs2FTILE9Y22YDRObIwVvMv_TlM14lfEYPoGgBgHNbV3KygeOuCSsbjkkppFQxkuqStgTGIZ7X2sk4I-oAP7cSprzwseD9JMiOErW91WApx5uU59Y"
                            alt="Farm View"
                            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                        />
                        <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to top, rgba(0,0,0,0.6), transparent)' }}></div>
                        <div style={{ position: 'absolute', bottom: '24px', left: '24px', color: 'white' }}>
                            <p style={{ fontSize: '1.25rem', fontWeight: 'bold', margin: 0 }}>Rabi Season 2024</p>
                            <p style={{ fontSize: '0.9rem', opacity: 0.9, margin: 0 }}>Optimized for Wheat & Mustard</p>
                        </div>
                    </div>

                    {/* Stats Grid */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginBottom: '32px' }}>
                        <StatBox icon={Users} label="Member Count" value="8" color="green" />
                        <StatBox icon={MapPin} label="Combined Acreage" value="60 Bigha" color="orange" />
                        <StatBox icon={Calendar} label="Selling Window" value="Nov 15-20" color="brown" />
                    </div>

                    {/* About Section */}
                    <div className="card" style={{ padding: '32px', marginBottom: '32px' }}>
                        <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '16px' }}>About the Group</h3>
                        <div style={{ color: 'var(--color-text-muted)', lineHeight: '1.6', fontSize: '1rem' }}>
                            <p style={{ marginBottom: '16px' }}>
                                This Land Pool Group (#402) is focused on the synchronized planting and harvesting of Wheat varieties suitable for the Ludhiana region. By pooling 60 Bigha of contiguous land, we have secured a contract for a Combine Harvester at 15% below market rate.
                            </p>
                            <p>
                                <strong>Requirements:</strong> Members must agree to the specified sowing window (Oct 25 - Nov 1) to ensure uniform crop maturity. All produce will be aggregated at the Raikot Collection Center.
                            </p>
                        </div>

                        <div style={{ marginTop: '24px', paddingTop: '24px', borderTop: '1px solid var(--color-border)' }}>
                            <h4 style={{ fontSize: '0.85rem', fontWeight: 'bold', textTransform: 'uppercase', color: 'var(--color-text-secondary)', marginBottom: '16px' }}>Pooled Land Location</h4>
                            <div style={{ borderRadius: '12px', overflow: 'hidden', border: '1px solid var(--color-border)', marginBottom: '24px' }}>
                                <MapComponent
                                    lat={30.9010}
                                    lon={75.8573}
                                    height="200px"
                                    zoom={14}
                                    markers={[{ lat: 30.9010, lon: 75.8573, popupText: "Pooled Land Area (60 Bigha)" }]}
                                />
                            </div>

                            <h4 style={{ fontSize: '0.85rem', fontWeight: 'bold', textTransform: 'uppercase', color: 'var(--color-text-secondary)', marginBottom: '16px' }}>Current Members</h4>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                <div style={{ display: 'flex', marginLeft: '12px' }}>
                                    {['RS', 'AK', 'SK', 'GS'].map((initials, i) => (
                                        <div key={i} style={{
                                            width: '40px',
                                            height: '40px',
                                            borderRadius: '50%',
                                            backgroundColor: i % 2 === 0 ? 'rgba(76,175,80,0.2)' : 'rgba(217,165,76,0.2)',
                                            color: i % 2 === 0 ? 'var(--color-primary-green)' : 'var(--color-accent-ochre)',
                                            border: '3px solid white',
                                            marginLeft: '-12px',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            fontSize: '0.85rem',
                                            fontWeight: 'bold'
                                        }}>{initials}</div>
                                    ))}
                                </div>
                                <span style={{ fontSize: '0.9rem', fontWeight: '500', color: 'var(--color-text-muted)' }}>+ 4 others joined recently</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Column: Actions */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                    <div className="card" style={{ position: 'sticky', top: '24px', backgroundColor: 'var(--color-card-brown)', border: '1px solid var(--color-border)' }}>
                        <h3 style={{ fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '4px' }}>Interested in joining?</h3>
                        <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', marginBottom: '24px' }}>Review the terms and apply to join this pool.</p>

                        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                            <button
                                onClick={onJoin}
                                style={{
                                    padding: '14px',
                                    backgroundColor: 'var(--color-primary-green)',
                                    color: 'white',
                                    fontSize: '1.1rem',
                                    fontWeight: 'bold',
                                    borderRadius: '12px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    gap: '8px',
                                    boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                                }}
                            >
                                <Users size={20} /> Join Group
                            </button>

                            <button style={{
                                padding: '14px',
                                backgroundColor: 'white',
                                color: 'var(--color-text-dark)',
                                border: '1px solid var(--color-border)',
                                fontSize: '1.1rem',
                                fontWeight: 'bold',
                                borderRadius: '12px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                gap: '8px'
                            }}>
                                <Mic size={20} color="var(--color-primary-green)" /> Ask Question via Voice
                            </button>
                        </div>

                        <div style={{ marginTop: '24px', paddingTop: '24px', borderTop: '1px solid rgba(0,0,0,0.05)' }}>
                            <div style={{ display: 'flex', alignItems: 'start', gap: '12px' }}>
                                <Check size={20} color="var(--color-accent-ochre)" />
                                <div>
                                    <p style={{ fontWeight: 'bold', margin: 0 }}>Secure Contract</p>
                                    <p style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)', margin: '4px 0 0 0' }}>Smart contracts ensure transparent profit sharing upon sale.</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="card" style={{ backgroundColor: 'white' }}>
                        <h3 style={{ fontSize: '0.85rem', fontWeight: 'bold', textTransform: 'uppercase', color: 'var(--color-text-secondary)', marginBottom: '16px' }}>Group Documents</h3>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                            <DocumentItem name="By-Laws.pdf" size="2.4 MB" icon={FileText} color="red" />
                            <DocumentItem name="Agreement_Draft.docx" size="1.1 MB" icon={FileText} color="blue" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

const StatBox = ({ icon: Icon, label, value, color }) => {
    const colors = {
        green: 'var(--color-primary-green)',
        orange: 'var(--color-accent-ochre)',
        brown: '#8D6E63'
    };
    const c = colors[color] || colors.green;

    return (
        <div style={{
            backgroundColor: 'var(--color-card-brown)',
            padding: '20px',
            borderRadius: '12px',
            border: '1px solid var(--color-border)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center'
        }}>
            <div style={{
                width: '48px',
                height: '48px',
                borderRadius: '50%',
                backgroundColor: `${c}33`, // 20% opacity approx
                color: c,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                marginBottom: '12px'
            }}>
                <Icon size={24} />
            </div>
            <p style={{ fontSize: '0.85rem', fontWeight: 'bold', textTransform: 'uppercase', color: 'var(--color-text-muted)', marginBottom: '4px' }}>{label}</p>
            <p style={{ fontSize: '1.5rem', fontWeight: '900', margin: 0, color: 'var(--color-text-dark)' }}>{value}</p>
        </div>
    );
};

const DocumentItem = ({ name, size, icon: Icon, color }) => (
    <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        padding: '12px',
        borderRadius: '8px',
        cursor: 'pointer',
        transition: 'background-color 0.2s',
    }}
        onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'var(--color-bg-beige)'}
        onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
    >
        <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '8px',
            backgroundColor: color === 'red' ? '#FFEBEE' : '#E3F2FD',
            color: color === 'red' ? '#D32F2F' : '#1976D2',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
        }}>
            <Icon size={20} />
        </div>
        <div style={{ flex: 1 }}>
            <p style={{ fontWeight: 'bold', fontSize: '0.9rem', margin: 0 }}>{name}</p>
            <p style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', margin: 0 }}>{size}</p>
        </div>
        <Download size={18} color="var(--color-text-muted)" />
    </div>
);

export default LandPoolDetails;
