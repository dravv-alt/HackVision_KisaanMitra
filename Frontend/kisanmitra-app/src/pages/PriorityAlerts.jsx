import React, { useState } from 'react';
import {
    Search,
    CloudRain,
    Bug,
    IndianRupee,
    TrendingDown,
    Sun,
    AlertTriangle,
    Sprout
} from 'lucide-react';
import '../styles/global.css';

const PriorityAlerts = () => {
    const [filter, setFilter] = useState('all');

    return (
        <div className="fade-in">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', marginBottom: '40px' }}>
                <div style={{ display: 'flex', alignItems: 'end', justifyContent: 'space-between', flexWrap: 'wrap', gap: '24px' }}>
                    <div>
                        <h2 style={{ fontSize: '2rem', fontWeight: '900', margin: 0, color: 'var(--color-text-dark)' }}>Priority Alerts</h2>
                        <p style={{ fontSize: '1.1rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>Real-time updates on Weather, Pests, and Mandi Prices.</p>
                    </div>
                    <div style={{ position: 'relative', width: '100%', maxWidth: '320px' }}>
                        <Search size={20} style={{ position: 'absolute', left: '12px', top: '12px', color: 'var(--color-text-muted)' }} />
                        <input
                            type="text"
                            placeholder="Search alerts..."
                            style={{
                                width: '100%',
                                padding: '12px 12px 12px 44px',
                                borderRadius: '12px',
                                border: '1px solid var(--color-border)',
                                outline: 'none',
                                fontSize: '1rem'
                            }}
                        />
                    </div>
                </div>

                <div style={{ display: 'flex', gap: '12px', overflowX: 'auto', paddingBottom: '4px' }}>
                    {['All Alerts', 'Weather', 'Pests', 'Mandi Prices'].map((f) => {
                        const isActive = filter === f.toLowerCase() || (filter === 'all' && f === 'All Alerts');
                        return (
                            <button
                                key={f}
                                onClick={() => setFilter(f.toLowerCase() === 'all alerts' ? 'all' : f.toLowerCase())}
                                style={{
                                    padding: '8px 20px',
                                    borderRadius: '20px',
                                    backgroundColor: isActive ? 'var(--color-primary-green)' : 'var(--color-bg-beige)',
                                    color: isActive ? 'white' : 'var(--color-text-muted)',
                                    border: isActive ? 'none' : '1px solid var(--color-border)',
                                    fontWeight: '600',
                                    whiteSpace: 'nowrap',
                                    cursor: 'pointer'
                                }}
                            >
                                {f}
                            </button>
                        );
                    })}
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '32px' }}>

                    {/* Alert 1 */}
                    <AlertCard
                        icon={CloudRain}
                        type="critical" // Red
                        tag="Critical"
                        title="Heavy Rain Warning"
                        desc="Heavy rainfall expected in next 4 hours. Secure harvested crops."
                        footerIcon={CloudRain}
                        footerText="Weather"
                        time="10 mins ago"
                    />

                    {/* Alert 2 */}
                    <AlertCard
                        icon={Bug}
                        type="warning" // Ochre
                        tag="Warning"
                        title="Pest Alert"
                        desc="Pest warning in neighboring village. Check leaves for white spots."
                        footerIcon={Bug}
                        footerText="Pest Control"
                        time="2 hours ago"
                    />

                    {/* Alert 3 */}
                    <AlertCard
                        icon={IndianRupee}
                        type="warning" // Ochre
                        tag="Warning"
                        title="Price Fluctuation"
                        desc="Mandi price for Wheat up by ₹50/quintal in local market."
                        footerIcon={IndianRupee}
                        footerText="Mandi"
                        time="4 hours ago"
                    />

                    {/* Alert 4 */}
                    <AlertCard
                        icon={Sprout} // Grass substitute
                        type="critical" // Red
                        tag="Critical"
                        title="Locust Swarm"
                        desc="Large swarm reported 20km north moving southwards."
                        footerIcon={AlertTriangle}
                        footerText="Pest Control"
                        time="30 mins ago"
                    />

                    {/* Alert 5 */}
                    <AlertCard
                        icon={TrendingDown}
                        type="critical" // Red
                        tag="Critical"
                        title="Price Crash"
                        desc="Tomato prices dropped by 15% unexpectedly this morning."
                        footerIcon={IndianRupee}
                        footerText="Mandi"
                        time="1 hour ago"
                    />

                    {/* Alert 6 */}
                    <AlertCard
                        icon={Sun}
                        type="warning" // Ochre
                        tag="Warning"
                        title="Heatwave Alert"
                        desc="Temperatures expected to cross 40°C. Ensure sufficient irrigation."
                        footerIcon={Sun}
                        footerText="Weather"
                        time="5 hours ago"
                    />

                    {/* Alert 7 - Info */}
                    <AlertCard
                        icon={Sprout}
                        type="info" // Blue
                        tag="Information"
                        title="Soil Health Card Renewal"
                        desc="Your soil health card expires in 15 days. Request a renewal."
                        footerIcon={AlertTriangle}
                        footerText="General"
                        time="1 day ago"
                    />

                    {/* Alert 8 - Info */}
                    <AlertCard
                        icon={IndianRupee}
                        type="info" // Blue
                        tag="Information"
                        title="New Scheme Announced"
                        desc="PM Kisan Samman Nidhi installment due next week."
                        footerIcon={IndianRupee}
                        footerText="Schemes"
                        time="2 days ago"
                    />

                </div>
            </div>
        </div>
    );
};

const AlertCard = ({ icon: Icon, type, tag, title, desc, footerIcon: FooterIcon, footerText, time }) => {

    // Theme Definitions
    const themes = {
        critical: {
            barColor: '#CB6E5D', // Terracotta Red
            iconColor: '#CB6E5D',
            tagBg: 'rgba(203, 110, 93, 0.1)',
            tagText: '#CB6E5D',
            hoverShadow: 'rgba(203, 110, 93, 0.15)'
        },
        warning: {
            barColor: '#D9A54C', // Ochre
            iconColor: '#D9A54C',
            tagBg: 'rgba(217, 165, 76, 0.1)',
            tagText: '#D9A54C',
            hoverShadow: 'rgba(217, 165, 76, 0.15)'
        },
        info: {
            barColor: '#4A90E2', // Blue
            iconColor: '#4A90E2',
            tagBg: 'rgba(74, 144, 226, 0.1)',
            tagText: '#4A90E2',
            hoverShadow: 'rgba(74, 144, 226, 0.15)'
        }
    };

    const theme = themes[type] || themes.info;

    return (
        <div className="card hover-scale-shadow" style={{
            padding: '24px',
            position: 'relative',
            overflow: 'hidden',
            display: 'flex',
            flexDirection: 'column',
            height: '100%',
            paddingLeft: '32px',
            border: '1px solid var(--color-border)',
            transition: 'all 0.3s ease'
        }}>
            <style>{`
                .hover-scale-shadow:hover {
                    box-shadow: 0 10px 25px -5px ${theme.hoverShadow}, 0 8px 10px -6px ${theme.hoverShadow};
                    transform: translateY(-2px);
                }
            `}</style>

            {/* Color Bar */}
            <div style={{ position: 'absolute', top: 0, left: 0, bottom: 0, width: '8px', backgroundColor: theme.barColor }}></div>

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
                <div style={{ padding: '12px', backgroundColor: 'white', borderRadius: '50%', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
                    <Icon size={32} color={theme.iconColor} />
                </div>
                <span style={{
                    padding: '4px 12px',
                    backgroundColor: theme.tagBg,
                    color: theme.tagText,
                    borderRadius: '20px',
                    fontSize: '0.75rem',
                    fontWeight: 'bold',
                    textTransform: 'uppercase',
                    border: `1px solid ${theme.tagBg}`
                }}>{tag}</span>
            </div>

            <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '8px', lineHeight: '1.3', color: 'var(--color-text-dark)' }}>{title}</h3>
            <p style={{ fontSize: '1.1rem', color: 'var(--color-text-muted)', lineHeight: '1.5', margin: '0 0 24px 0' }}>{desc}</p>

            <div style={{ marginTop: 'auto', paddingTop: '16px', borderTop: '1px solid var(--color-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <FooterIcon size={16} /> {footerText}
                </div>
                <span>{time}</span>
            </div>
        </div>
    );
};

export default PriorityAlerts;
