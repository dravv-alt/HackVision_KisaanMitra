import React from 'react';
import { Droplet, Calendar, TrendingUp, AlertTriangle, ArrowRight } from 'lucide-react';

const CropCard = ({ data }) => {
    // data format: { name, season, water, duration, expected, risk }
    return (
        <div className="smart-card">
            {/* Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px', borderBottom: '1px solid var(--card-border)', paddingBottom: '12px' }}>
                <div style={{ fontSize: '1.5rem' }}>🌾</div>
                <div>
                    <h3 style={{ margin: 0, fontSize: '1.2rem', color: 'var(--text-primary)' }}>{data.name}</h3>
                    <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Recommended for your farm</span>
                </div>
            </div>

            {/* Stats Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <StatRow icon={Droplet} label="Water Need" value={data.water} />
                <StatRow icon={Calendar} label="Duration" value={data.duration} />
                <StatRow icon={TrendingUp} label="Expected" value={data.expected} />
                <StatRow icon={AlertTriangle} label="Risk Level" value={data.risk} />
            </div>

            {/* CTA */}
            <button className="card-cta">
                View Full Details <ArrowRight size={16} />
            </button>
        </div>
    );
};

const StatRow = ({ icon: Icon, label, value }) => (
    <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '2px' }}>
            <Icon size={14} /> {label}
        </div>
        <div style={{ fontSize: '0.95rem', fontWeight: '500', color: 'var(--text-primary)' }}>{value}</div>
    </div>
);

export default CropCard;
