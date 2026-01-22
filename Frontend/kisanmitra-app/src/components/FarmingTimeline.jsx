import React from 'react';
import {
    Calendar,
    Leaf,
    Droplet,
    Bug,
    TrendingUp,
    Sun,
    Package
} from 'lucide-react';
import '../styles/global.css';

const FarmingTimeline = () => {
    return (
        <div className="fade-in">
            <div style={{ display: 'flex', flexDirection: 'column', mdDirection: 'row', alignItems: 'flex-start', justifyContent: 'space-between', gap: '24px', marginBottom: '48px' }}>
                <div>
                    <h2 style={{ fontSize: '2rem', fontWeight: '900', margin: '0 0 8px 0', color: 'var(--color-text-dark)' }}>Farming Lifecycle</h2>
                    <p style={{ fontSize: '1.1rem', color: 'var(--color-text-muted)', margin: 0 }}>Your upcoming tasks and crop milestones.</p>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 16px', backgroundColor: 'var(--color-bg-beige)', borderRadius: '8px', border: '1px solid var(--color-border)', fontSize: '0.9rem', fontWeight: '500', color: 'var(--color-text-muted)' }}>
                    <Calendar size={18} color="var(--color-primary-green)" />
                    October 2023 - November 2023
                </div>
            </div>

            <div className="timeline-wrapper" style={{ position: 'relative', width: '100%', maxWidth: '1000px', margin: '0 auto', padding: '20px 0' }}>
                {/* Center Line for Desktop */}
                <div style={{ position: 'absolute', left: '50%', top: 0, bottom: 0, width: '2px', backgroundColor: '#E0E0E0', transform: 'translateX(-50%)' }} className="timeline-line-desktop"></div>
                {/* Left Line for Mobile */}
                <div style={{ position: 'absolute', left: '20px', top: 0, bottom: 0, width: '2px', backgroundColor: '#E0E0E0' }} className="timeline-line-mobile"></div>

                <style>{`
                    @media (min-width: 768px) {
                        .timeline-line-desktop { display: block !important; }
                        .timeline-line-mobile { display: none !important; }
                        .timeline-row { display: flex !important; justify-content: space-between; align-items: center; width: 100%; margin-bottom: 40px; position: relative; }
                        .timeline-row .content-side { width: 45%; }
                        .timeline-row .empty-side { width: 45%; }
                        .center-dot { position: absolute !important; left: 50% !important; transform: translateX(-50%) !important; top: 50% !important; margin-top: -10px; }
                        
                        /* Left aligned item */
                        .timeline-row.left .content-side { order: 1; text-align: right; display: flex; justify-content: flex-end; }
                        .timeline-row.left .empty-side { order: 3; }
                        
                        /* Right aligned item */
                        .timeline-row.right .empty-side { order: 1; }
                        .timeline-row.right .content-side { order: 3; text-align: left; display: flex; justify-content: flex-start; }

                        .card-inner { width: 100%; max-width: 450px; }
                    }
                    
                    @media (max-width: 767px) {
                        .timeline-line-desktop { display: none !important; }
                         .timeline-line-mobile { display: block !important; }
                        .timeline-row { display: flex; flex-direction: column; padding-left: 50px; position: relative; margin-bottom: 40px; }
                        .center-dot { position: absolute; left: 11px; top: 24px; } 
                        .content-side { width: 100%; }
                        .empty-side { display: none; }
                        .card-inner { width: 100%; }
                    }
                `}</style>

                {/* --- Row 1: Wheat (Left) --- */}
                <div className="timeline-row left">
                    <div className="content-side">
                        <div className="card card-inner" style={{ padding: '24px', textAlign: 'left' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '8px' }}>
                                <span style={{ padding: '4px 8px', backgroundColor: '#E3F2FD', color: '#1565C0', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase' }}>Wheat</span>
                                <span style={{ fontSize: '0.9rem', fontWeight: 'bold', color: 'var(--color-text-muted)' }}>Oct 28</span>
                            </div>
                            <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', margin: '0 0 4px 0', color: 'var(--color-text-dark)' }}>Fertilizer Application</h3>
                            <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', margin: '0 0 16px 0' }}>Apply NPK mix for initial growth boost.</p>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px', backgroundColor: 'white', borderRadius: '8px', border: '1px solid #eee', fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>
                                <Leaf size={16} /> Recommended: 50kg/acre
                            </div>
                        </div>
                    </div>
                    <div className="center-dot" style={{ width: '20px', height: '20px', backgroundColor: 'var(--color-bg-beige)', border: '4px solid #42A5F5', borderRadius: '50%', zIndex: 2 }}></div>
                    <div className="empty-side"></div>
                </div>

                {/* --- Row 2: Paddy (Right) --- */}
                <div className="timeline-row right">
                    <div className="empty-side"></div>
                    <div className="center-dot" style={{ width: '20px', height: '20px', backgroundColor: 'var(--color-bg-beige)', border: '4px solid var(--color-primary-green)', borderRadius: '50%', zIndex: 2 }}></div>
                    <div className="content-side">
                        <div className="card card-inner" style={{ padding: '24px', textAlign: 'left' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '8px' }}>
                                <span style={{ padding: '4px 8px', backgroundColor: '#E8F5E9', color: '#2E7D32', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase' }}>Paddy</span>
                                <span style={{ fontSize: '0.9rem', fontWeight: 'bold', color: 'var(--color-text-muted)' }}>Oct 30</span>
                            </div>
                            <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', margin: '0 0 4px 0', color: 'var(--color-text-dark)' }}>Irrigation Schedule</h3>
                            <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', margin: '0 0 16px 0' }}>Critical water level maintenance phase.</p>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px', backgroundColor: 'white', borderRadius: '8px', border: '1px solid #eee', fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>
                                <Droplet size={16} /> Maintain 5cm depth
                            </div>
                        </div>
                    </div>
                </div>

                {/* --- Row 3: Mustard (Left) --- */}
                <div className="timeline-row left">
                    <div className="content-side">
                        <div className="card card-inner" style={{ padding: '24px', textAlign: 'left' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '8px' }}>
                                <span style={{ padding: '4px 8px', backgroundColor: '#FFF3E0', color: '#EF6C00', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase' }}>Mustard</span>
                                <span style={{ fontSize: '0.9rem', fontWeight: 'bold', color: 'var(--color-text-muted)' }}>Nov 05</span>
                            </div>
                            <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', margin: '0 0 4px 0', color: 'var(--color-text-dark)' }}>Pest Monitoring</h3>
                            <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', margin: '0 0 16px 0' }}>Check for early signs of aphids.</p>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px', backgroundColor: 'white', borderRadius: '8px', border: '1px solid #eee', fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>
                                <Bug size={16} /> Inspect leaf undersides
                            </div>
                        </div>
                    </div>
                    <div className="center-dot" style={{ width: '20px', height: '20px', backgroundColor: 'var(--color-bg-beige)', border: '4px solid #FFA726', borderRadius: '50%', zIndex: 2 }}></div>
                    <div className="empty-side"></div>
                </div>

                {/* --- Row 4: Soybean (Right) --- */}
                <div className="timeline-row right">
                    <div className="empty-side"></div>
                    <div className="center-dot" style={{ width: '20px', height: '20px', backgroundColor: 'var(--color-bg-beige)', border: '4px solid var(--color-accent-ochre)', borderRadius: '50%', zIndex: 2 }}></div>
                    <div className="content-side">
                        <div className="card card-inner" style={{ padding: '24px', textAlign: 'left', border: '2px solid var(--color-accent-ochre)' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '8px' }}>
                                <span style={{ padding: '4px 8px', backgroundColor: '#FFF8E1', color: '#F57F17', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase' }}>Soybean</span>
                                <span style={{ fontSize: '0.9rem', fontWeight: 'bold', color: 'var(--color-text-muted)' }}>Nov 15</span>
                            </div>
                            <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', margin: '0 0 4px 0', color: 'var(--color-text-dark)' }}>Harvest Window</h3>
                            <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', margin: '0 0 16px 0' }}>Optimal moisture content expected.</p>
                            <div style={{ display: 'flex', gap: '12px' }}>
                                <button style={{ flex: 1, padding: '10px', backgroundColor: 'var(--color-accent-ochre)', color: 'white', borderRadius: '8px', fontWeight: '600', border: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                                    <Package size={16} /> Book
                                </button>
                                <button style={{ flex: 1, padding: '10px', backgroundColor: 'transparent', border: '1px solid var(--color-border)', borderRadius: '8px', fontWeight: '600', color: 'var(--color-text-dark)' }}>Details</button>
                            </div>
                        </div>
                    </div>
                </div>

            </div>

            {/* Bottom Stats Grid */}
            <div style={{ marginTop: '64px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '24px' }}>
                <BottomStatCard
                    icon={Sun} iconBg="rgba(76, 175, 80, 0.2)" iconColor="var(--color-primary-green)"
                    label="Weather Forecast"
                    value="Clear Sky for 3 Days"
                    borderColor="var(--color-primary-green)"
                />
                <BottomStatCard
                    icon={TrendingUp} iconBg="rgba(217, 165, 76, 0.2)" iconColor="var(--color-accent-ochre)"
                    label="Market Price Trend"
                    value="Wheat up by 2%"
                    borderColor="var(--color-accent-ochre)"
                />
                <BottomStatCard
                    icon={Package} iconBg="#E3F2FD" iconColor="#1565C0"
                    label="Inventory Status"
                    value="Seeds Low Stock"
                    borderColor="#1565C0"
                />
            </div>
        </div>
    );
};

const BottomStatCard = ({ icon: Icon, iconBg, iconColor, label, value, borderColor }) => (
    <div style={{
        padding: '24px',
        borderRadius: '16px',
        backgroundColor: `${iconBg.replace('0.2', '0.05')}`, // faint bg
        border: `1px solid ${borderColor}40`,
        display: 'flex',
        alignItems: 'center',
        gap: '16px'
    }}>
        <div style={{
            width: '48px',
            height: '48px',
            borderRadius: '50%',
            backgroundColor: iconBg,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: iconColor
        }}>
            <Icon size={24} />
        </div>
        <div>
            <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', fontWeight: '500', margin: 0 }}>{label}</p>
            <p style={{ fontSize: '1.1rem', fontWeight: 'bold', color: 'var(--color-text-dark)', margin: 0 }}>{value}</p>
        </div>
    </div>
);

export default FarmingTimeline;
