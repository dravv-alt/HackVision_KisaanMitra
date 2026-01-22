import React from 'react';
import {
    ArrowLeft,
    MapPin,
    Users,
    Check,
    Handshake,
    Truck,
    DollarSign,
    TrendingUp,
    Calendar,
    Clock,
    AlertTriangle,
    UserPlus,
    Gavel,
    Share2
} from 'lucide-react';
import '../styles/global.css';

const ActivePoolDashboard = ({ onBack }) => {
    return (
        <div>
            {/* Header */}
            <div style={{ marginBottom: '24px' }}>
                <button
                    onClick={onBack}
                    style={{
                        background: 'none',
                        padding: '0',
                        marginBottom: '16px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        color: 'var(--color-text-muted)'
                    }}
                >
                    <ArrowLeft size={20} /> Back to Pools
                </button>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <span style={{
                            padding: '4px 12px',
                            backgroundColor: '#E8F5E9',
                            color: 'var(--color-primary-green)',
                            borderRadius: '20px',
                            fontSize: '0.8rem',
                            fontWeight: 'bold',
                            border: '1px solid var(--color-primary-green)'
                        }}>
                            ACTIVE GROUP
                        </span>
                        <span style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>• Wheat Collective</span>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', flexWrap: 'wrap', gap: '16px' }}>
                        <h2 style={{ fontSize: '1.8rem', margin: 0, fontWeight: '800' }}>Ludhiana Wheat Pool #24</h2>

                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <div style={{ display: 'flex', marginLeft: '12px' }}>
                                {[1, 2, 3].map(i => (
                                    <div key={i} style={{
                                        width: '32px',
                                        height: '32px',
                                        borderRadius: '50%',
                                        backgroundColor: '#ddd',
                                        border: '2px solid white',
                                        marginLeft: '-12px',
                                        backgroundImage: `url(https://placehold.co/100x100?text=${i})`,
                                        backgroundSize: 'cover'
                                    }}></div>
                                ))}
                                <div style={{
                                    width: '32px',
                                    height: '32px',
                                    borderRadius: '50%',
                                    backgroundColor: 'var(--color-card-brown)',
                                    border: '2px solid white',
                                    marginLeft: '-12px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    fontSize: '0.7rem',
                                    fontWeight: 'bold'
                                }}>+12</div>
                            </div>
                            <button style={{ padding: '8px', borderRadius: '8px', border: '1px solid var(--color-border)' }}>
                                <Share2 size={20} color="var(--color-text-muted)" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Progress Steps */}
            <div className="card" style={{ marginBottom: '24px', overflowX: 'auto' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', minWidth: '600px', position: 'relative' }}>
                    {/* Connecting Line */}
                    <div style={{
                        position: 'absolute',
                        top: '20px',
                        left: '0',
                        width: '100%',
                        height: '4px',
                        backgroundColor: '#eee',
                        zIndex: 0
                    }}>
                        <div style={{ width: '60%', height: '100%', backgroundColor: 'var(--color-primary-green)' }}></div>
                    </div>

                    {[
                        { label: 'Formation', icon: Check, status: 'completed' },
                        { label: 'Aggregation', icon: Check, status: 'completed' },
                        { label: 'Negotiation', icon: Handshake, status: 'active' },
                        { label: 'Logistics', icon: Truck, status: 'pending' },
                        { label: 'Payment', icon: DollarSign, status: 'pending' },
                    ].map((step, idx) => (
                        <div key={idx} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', zIndex: 1 }}>
                            <div style={{
                                width: '40px',
                                height: '40px',
                                borderRadius: '50%',
                                backgroundColor: step.status === 'completed' || step.status === 'active' ? 'var(--color-primary-green)' : 'var(--color-bg-beige)',
                                color: step.status === 'completed' || step.status === 'active' ? 'white' : 'var(--color-text-muted)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                boxShadow: step.status === 'active' ? '0 0 0 4px rgba(76, 175, 80, 0.2)' : 'none'
                            }}>
                                <step.icon size={20} />
                            </div>
                            <span style={{
                                fontSize: '0.85rem',
                                fontWeight: 'bold',
                                color: step.status === 'pending' ? 'var(--color-text-muted)' : 'var(--color-primary-green)'
                            }}>
                                {step.label}
                            </span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Main Status Cards Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginBottom: '32px' }}>

                {/* Card 1: Negotiation Stage */}
                <div className="card" style={{ position: 'relative', overflow: 'hidden' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
                        <div style={{ padding: '8px', backgroundColor: '#FAFAFA', borderRadius: '8px', border: '1px solid #eee' }}>
                            <Handshake size={24} color="var(--color-primary-green)" />
                        </div>
                        <span style={{
                            padding: '4px 8px',
                            backgroundColor: '#FFF8E1',
                            color: '#F57F17',
                            borderRadius: '12px',
                            fontSize: '0.75rem',
                            fontWeight: 'bold',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '4px'
                        }}>
                            In Progress
                        </span>
                    </div>
                    <h4 style={{ textTransform: 'uppercase', color: 'var(--color-text-muted)', fontSize: '0.75rem', fontWeight: 'bold' }}>Current Stage</h4>
                    <p style={{ fontSize: '1.5rem', fontWeight: '900', margin: '4px 0 8px 0' }}>Negotiation</p>
                    <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem', marginBottom: '24px' }}>Talking to 3 potential buyers from major retail chains.</p>

                    <div>
                        <div style={{ width: '100%', height: '8px', backgroundColor: '#eee', borderRadius: '4px', marginBottom: '8px' }}>
                            <div style={{ width: '65%', height: '100%', backgroundColor: '#F57F17', borderRadius: '4px' }}></div>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>
                            <span>Progress</span>
                            <span>65% Complete</span>
                        </div>
                    </div>
                </div>

                {/* Card 2: Price Target */}
                <div className="card">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
                        <div style={{ padding: '8px', backgroundColor: '#FAFAFA', borderRadius: '8px', border: '1px solid #eee' }}>
                            <TrendingUp size={24} color="var(--color-primary-green)" />
                        </div>
                        <span style={{
                            padding: '4px 8px',
                            backgroundColor: '#E8F5E9',
                            color: 'var(--color-primary-green)',
                            borderRadius: '12px',
                            fontSize: '0.75rem',
                            fontWeight: 'bold'
                        }}>
                            +15% vs Market
                        </span>
                    </div>
                    <h4 style={{ textTransform: 'uppercase', color: 'var(--color-text-muted)', fontSize: '0.75rem', fontWeight: 'bold' }}>Target Price</h4>
                    <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px', margin: '4px 0 8px 0' }}>
                        <span style={{ fontSize: '1.5rem', fontWeight: '900' }}>₹2,100</span>
                        <span style={{ color: 'var(--color-text-muted)' }}>/ quintal</span>
                    </div>
                    <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem', marginBottom: '24px' }}>
                        Current highest bid: <strong>₹2,050/q</strong> by Reliance Retail.
                    </p>
                    <button style={{ width: '100%', padding: '8px', border: '1px solid var(--color-border)', borderRadius: '8px', fontWeight: '600' }}>
                        View Bids
                    </button>
                </div>

                {/* Card 3: Next Action */}
                <div className="card" style={{ borderLeft: '4px solid #FBC02D' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
                        <div style={{ padding: '8px', backgroundColor: '#FAFAFA', borderRadius: '8px', border: '1px solid #eee' }}>
                            <Truck size={24} color="#FBC02D" />
                        </div>
                        <span style={{
                            padding: '4px 8px',
                            backgroundColor: '#FFEBEE',
                            color: '#D32F2F',
                            borderRadius: '12px',
                            fontSize: '0.75rem',
                            fontWeight: 'bold'
                        }}>
                            Action Needed
                        </span>
                    </div>
                    <h4 style={{ textTransform: 'uppercase', color: 'var(--color-text-muted)', fontSize: '0.75rem', fontWeight: 'bold' }}>Next Action</h4>
                    <p style={{ fontSize: '1.25rem', fontWeight: '900', margin: '4px 0 4px 0' }}>Transport Booking</p>
                    <p style={{ color: '#F57F17', fontSize: '0.9rem', fontWeight: 'bold', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Calendar size={16} /> Due by Oct 30
                    </p>
                    <button style={{ width: '100%', padding: '10px', backgroundColor: 'var(--color-primary-green)', color: 'white', borderRadius: '8px', fontWeight: 'bold' }}>
                        Review Logistics
                    </button>
                </div>
            </div>

            {/* Activity Feed & Summary */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>

                {/* Activity Feed */}
                <div className="card">
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
                        <h3 style={{ fontSize: '1.2rem', margin: 0 }}>Recent Activity</h3>
                        <button style={{ color: 'var(--color-primary-green)', fontWeight: 'bold', fontSize: '0.9rem' }}>View All</button>
                    </div>

                    <div style={{ display: 'flex', gap: '12px', borderBottom: '1px solid var(--color-border)', paddingBottom: '16px', marginBottom: '16px' }}>
                        <div style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: '#F3E5F5', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <Gavel size={20} color="#7B1FA2" />
                        </div>
                        <div>
                            <div style={{ fontWeight: 'bold' }}>New bid received</div>
                            <div style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>Reliance Retail placed a bid of ₹2,050/quintal.</div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>2 hours ago</div>
                        </div>
                    </div>

                    <div style={{ display: 'flex', gap: '12px', borderBottom: '1px solid var(--color-border)', paddingBottom: '16px', marginBottom: '16px' }}>
                        <div style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: '#FFF3E0', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <AlertTriangle size={20} color="#EF6C00" />
                        </div>
                        <div>
                            <div style={{ fontWeight: 'bold' }}>Quality check required</div>
                            <div style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>Sample testing scheduled for Lot #4 pending.</div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>5 hours ago</div>
                        </div>
                    </div>

                    <div style={{ display: 'flex', gap: '12px' }}>
                        <div style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: '#E3F2FD', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <UserPlus size={20} color="#1976D2" />
                        </div>
                        <div>
                            <div style={{ fontWeight: 'bold' }}>New member joined</div>
                            <div style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>Ramesh Singh added 50 quintals to the pool.</div>
                            <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>Yesterday</div>
                        </div>
                    </div>
                </div>

                {/* Pool Summary */}
                <div style={{
                    backgroundColor: '#E8F5E9',
                    borderRadius: '16px',
                    padding: '24px',
                    position: 'relative',
                    overflow: 'hidden',
                    border: '1px solid rgba(76, 175, 80, 0.2)'
                }}>
                    {/* Decorative Blur */}
                    <div style={{ position: 'absolute', bottom: '-20px', right: '-20px', width: '120px', height: '120px', backgroundColor: 'var(--color-primary-green)', opacity: '0.1', borderRadius: '50%', filter: 'blur(40px)' }}></div>

                    <h3 style={{ margin: '0 0 24px 0' }}>Pool Summary</h3>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', position: 'relative', zIndex: 1 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <span style={{ color: 'var(--color-text-muted)' }}>Total Quantity</span>
                            <span style={{ fontWeight: 'bold' }}>450 Quintals</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <span style={{ color: 'var(--color-text-muted)' }}>Participating Farmers</span>
                            <span style={{ fontWeight: 'bold' }}>15</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <span style={{ color: 'var(--color-text-muted)' }}>Est. Total Value</span>
                            <span style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>₹9,45,000</span>
                        </div>
                    </div>

                    <div style={{ marginTop: '24px', paddingTop: '16px', borderTop: '1px solid rgba(0,0,0,0.1)', fontStyle: 'italic', fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>
                        "Pooling resources increases bargaining power by approximately 18%."
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ActivePoolDashboard;
