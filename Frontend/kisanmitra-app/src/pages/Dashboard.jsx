import React from 'react';
import { Link } from 'react-router-dom';
import {
    CloudSun,
    Droplet,
    Wind,
    Sprout,
    Store,
    TrendingUp,
    TrendingDown,
    Minus,
    Wallet,
    ShoppingCart,
    Bell,
    AlertTriangle,
    Bug,
    CalendarClock,
    ChevronRight,
    MapPin
} from 'lucide-react';
import FarmingTimeline from '../components/FarmingTimeline';
import '../styles/global.css';

const Dashboard = () => {
    return (
        <div className="fade-in" style={{ paddingBottom: '80px' }}>

            {/* Header / Welcome Section */}
            <div style={{ display: 'flex', flexDirection: 'column', mdDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-end', gap: '24px', marginBottom: '40px' }}>
                <div>
                    <h2 style={{ fontSize: '2.5rem', fontWeight: '900', margin: '0 0 8px 0', color: 'var(--color-text-dark)' }}>Namaste, Ramesh</h2>
                    <p style={{ fontSize: '1.2rem', color: 'var(--color-text-muted)', margin: 0 }}>Here's the summary for your farm today.</p>
                </div>

                {/* Weather Widget */}
                <div className="card" style={{ padding: '16px 24px', display: 'flex', alignItems: 'center', gap: '24px', borderRadius: '16px', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }}>
                    <div style={{ paddingRight: '24px', borderRight: '1px solid var(--color-border)', display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <CloudSun size={32} color="var(--color-accent-ochre)" />
                        <div>
                            <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>32°C</div>
                            <div style={{ fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase', color: 'var(--color-text-muted)' }}>SUNNY</div>
                        </div>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <Droplet size={24} color="var(--color-primary-green)" />
                        <div>
                            <div style={{ fontSize: '1.25rem', fontWeight: 'bold' }}>10%</div>
                            <div style={{ fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase', color: 'var(--color-text-muted)' }}>CHANCE OF RAIN</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Main Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '32px', marginBottom: '48px' }}>

                {/* Active Crops Summary */}
                <Link to="/active-crops" style={{ textDecoration: 'none', color: 'inherit' }}>
                    <div className="card hover-scale" style={{ display: 'flex', flexDirection: 'column', height: '100%', cursor: 'pointer', transition: 'transform 0.2s' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                <div style={{ padding: '8px', backgroundColor: 'rgba(76, 175, 80, 0.1)', borderRadius: '8px', color: 'var(--color-primary-green)' }}>
                                    <Sprout size={24} />
                                </div>
                                <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', margin: 0 }}>Active Crops</h3>
                            </div>
                            <span style={{ fontSize: '0.9rem', fontWeight: '600', color: 'var(--color-primary-green)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                                View Field <ChevronRight size={16} />
                            </span>
                        </div>

                        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                            <CropRow name="Wheat (Rabi)" status="Healthy" statusColor="green" planted="45 days ago" iconChar="W" iconBg="#E8F5E9" iconColor="#2E7D32" />
                            <CropRow name="Mustard" status="Needs Water" statusColor="yellow" planted="Flowering Stage" iconChar="M" iconBg="#FFF8E1" iconColor="#F57F17" />
                            <CropRow name="Potato" status="Monitoring" statusColor="gray" planted="Harvest in 2 weeks" iconChar="P" iconBg="#EFEBE9" iconColor="#5D4037" />
                        </div>
                    </div>
                </Link>

                {/* Mandi Prices */}
                <div className="card" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <div style={{ padding: '8px', backgroundColor: 'rgba(217, 165, 76, 0.1)', borderRadius: '8px', color: 'var(--color-accent-ochre)' }}>
                                <Store size={24} />
                            </div>
                            <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', margin: 0 }}>Mandi Prices</h3>
                        </div>
                        <span style={{ fontSize: '0.8rem', fontWeight: '500', padding: '4px 8px', backgroundColor: '#f5f5f5', borderRadius: '4px' }}>Updated 2h ago</span>
                    </div>

                    <div style={{ overflowX: 'auto', border: '1px solid var(--color-border)', borderRadius: '12px' }}>
                        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
                            <thead style={{ backgroundColor: '#EBE5D5' }}>
                                <tr>
                                    <th style={{ textAlign: 'left', padding: '12px 16px', color: 'var(--color-text-muted)', fontSize: '0.8rem', textTransform: 'uppercase' }}>Crop</th>
                                    <th style={{ textAlign: 'left', padding: '12px 16px', color: 'var(--color-text-muted)', fontSize: '0.8rem', textTransform: 'uppercase' }}>Price / Quintal</th>
                                    <th style={{ textAlign: 'right', padding: '12px 16px', color: 'var(--color-text-muted)', fontSize: '0.8rem', textTransform: 'uppercase' }}>Trend</th>
                                </tr>
                            </thead>
                            <tbody>
                                <PriceRow crop="Wheat (Sharbati)" price="₹2,850" trend="+2.4%" trendDir="up" />
                                <PriceRow crop="Mustard Seeds" price="₹5,400" trend="-1.2%" trendDir="down" />
                                <PriceRow crop="Soybean" price="₹4,200" trend="0.0%" trendDir="neutral" isLast />
                            </tbody>
                        </table>
                    </div>
                    <div style={{ textAlign: 'center', marginTop: '16px' }}>
                        <a href="#" style={{ fontSize: '0.9rem', color: 'var(--color-primary-green)', fontWeight: '600', textDecoration: 'none' }}>View all market rates</a>
                    </div>
                </div>

                {/* Financial Overview */}
                <div className="card" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                            <div style={{ padding: '8px', backgroundColor: 'rgba(76, 175, 80, 0.1)', borderRadius: '8px', color: 'var(--color-primary-green)' }}>
                                <Wallet size={24} />
                            </div>
                            <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', margin: 0 }}>Financial Overview</h3>
                        </div>
                        <select style={{ border: 'none', backgroundColor: 'transparent', fontWeight: '600', color: 'var(--color-text-muted)', cursor: 'pointer' }}>
                            <option>This Month</option>
                        </select>
                    </div>

                    <div style={{ display: 'flex', gap: '16px', height: '100%' }}>
                        <FinanceCard
                            title="Total Revenue"
                            amount="₹1,24,500"
                            barPercent="75%"
                            barColor="var(--color-primary-green)"
                            change="+12% from last month"
                            changeColor="var(--color-primary-green)"
                            icon={TrendingUp}
                        />
                        <FinanceCard
                            title="Total Expenses"
                            amount="₹45,200"
                            barPercent="40%"
                            barColor="#D9724C"
                            change="Mainly fertilizers & labor"
                            changeColor="var(--color-text-muted)"
                            icon={ShoppingCart}
                        />
                    </div>
                </div>

                {/* Priority Alerts */}
                <Link to="/alerts" style={{ textDecoration: 'none', color: 'inherit' }}>
                    <div className="card hover-scale" style={{ display: 'flex', flexDirection: 'column', height: '100%', cursor: 'pointer', transition: 'transform 0.2s' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                <div style={{ padding: '8px', backgroundColor: 'rgba(217, 114, 76, 0.1)', borderRadius: '8px', color: '#D9724C' }}>
                                    <Bell size={24} />
                                </div>
                                <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', margin: 0 }}>Priority Alerts</h3>
                            </div>
                            <span style={{ backgroundColor: '#FFEBEE', color: '#D32F2F', fontSize: '0.75rem', fontWeight: 'bold', padding: '4px 10px', borderRadius: '12px' }}>2 New</span>
                        </div>

                        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                            <AlertRow
                                title="Heavy Rain Warning"
                                desc="Expected in next 24 hours. Secure harvested crops."
                                type="critical"
                                icon={AlertTriangle}
                            />
                            <AlertRow
                                title="Pest Alert: Aphids"
                                desc="Detected in nearby farms. Check mustard crop."
                                type="warning"
                                icon={Bug}
                            />

                        </div>
                    </div>
                </Link>
            </div>

            {/* Timeline Section (Screen 4) */}
            <FarmingTimeline />

        </div>
    );
};

// Helper Components
const CropRow = ({ name, status, statusColor, planted, iconChar, iconBg, iconColor }) => {
    let badgeBg, badgeText;
    if (statusColor === 'green') { badgeBg = '#E8F5E9'; badgeText = '#2E7D32'; }
    else if (statusColor === 'yellow') { badgeBg = '#FFF8E1'; badgeText = '#F57F17'; }
    else { badgeBg = '#F5F5F5'; badgeText = '#616161'; }

    return (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px', borderRadius: '12px', backgroundColor: 'white', border: '1px solid transparent' }} className="hover-border-primary">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: iconBg, color: iconColor, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>
                    {iconChar}
                </div>
                <div>
                    <div style={{ fontWeight: 'bold', fontSize: '1rem' }}>{name}</div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>{planted}</div>
                </div>
            </div>
            <span style={{ backgroundColor: badgeBg, color: badgeText, fontSize: '0.75rem', fontWeight: 'bold', padding: '4px 10px', borderRadius: '12px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                {status === 'Needs Water' && <Droplet size={12} />}
                {status}
            </span>
        </div>
    );
};

const PriceRow = ({ crop, price, trend, trendDir, isLast }) => (
    <tr style={{ borderBottom: isLast ? 'none' : '1px solid var(--color-border)' }}>
        <td style={{ padding: '12px 16px', fontWeight: '500' }}>{crop}</td>
        <td style={{ padding: '12px 16px' }}>{price}</td>
        <td style={{ padding: '12px 16px', textAlign: 'right' }}>
            <span style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
                padding: '2px 8px',
                borderRadius: '12px',
                fontSize: '0.8rem',
                fontWeight: 'bold',
                backgroundColor: trendDir === 'up' ? '#E8F5E9' : trendDir === 'down' ? '#FFEBEE' : '#F5F5F5',
                color: trendDir === 'up' ? '#2E7D32' : trendDir === 'down' ? '#D32F2F' : '#616161'
            }}>
                {trendDir === 'up' && <TrendingUp size={12} />}
                {trendDir === 'down' && <TrendingDown size={12} />}
                {trendDir === 'neutral' && <Minus size={12} />}
                {trend}
            </span>
        </td>
    </tr>
);

const FinanceCard = ({ title, amount, barPercent, barColor, change, changeColor, icon: Icon }) => (
    <div style={{ flex: 1, backgroundColor: 'white', padding: '20px', borderRadius: '12px', border: '1px solid var(--color-border)', position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', top: '16px', right: '16px', opacity: 0.1 }}>
            <Icon size={48} color={changeColor} />
        </div>
        <div style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', marginBottom: '4px' }}>{title}</div>
        <div style={{ fontSize: '1.5rem', fontWeight: '900', marginBottom: '16px' }}>{amount}</div>
        <div style={{ width: '100%', height: '6px', backgroundColor: '#f0f0f0', borderRadius: '3px', marginBottom: '8px', overflow: 'hidden' }}>
            <div style={{ width: barPercent, height: '100%', backgroundColor: barColor }}></div>
        </div>
        <div style={{ fontSize: '0.75rem', fontWeight: 'bold', color: changeColor }}>{change}</div>
    </div>
);

const AlertRow = ({ title, desc, type, icon: Icon }) => {
    let borderLeft, bg, iconColor;
    if (type === 'critical') { borderLeft = '#D32F2F'; bg = '#FFEBEE'; iconColor = '#D32F2F'; }
    else if (type === 'warning') { borderLeft = 'var(--color-accent-ochre)'; bg = '#FFFDE7'; iconColor = 'var(--color-accent-ochre)'; }
    else { borderLeft = '#2196F3'; bg = '#E3F2FD'; iconColor = '#2196F3'; }

    return (
        <div style={{
            display: 'flex',
            gap: '12px',
            padding: '16px',
            backgroundColor: bg,
            borderLeft: `4px solid ${borderLeft}`,
            borderRadius: '0 12px 12px 0'
        }}>
            <Icon size={20} color={iconColor} style={{ marginTop: '2px' }} />
            <div>
                <div style={{ fontSize: '0.9rem', fontWeight: 'bold', color: 'var(--color-text-dark)' }}>{title}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)', marginTop: '2px' }}>{desc}</div>
            </div>
        </div>
    );
};

export default Dashboard;
