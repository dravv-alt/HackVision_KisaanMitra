import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import '../styles/voice-interface.css';

const MarketPriceCard = ({ crop, price, trend, trendValue, trendDir, lastUpdated }) => {

    // Determine trend styles
    let trendColor = 'var(--color-text-muted)';
    let TrendIcon = Minus;
    let trendText = 'Stable';

    if (trendDir === 'up') {
        trendColor = 'var(--color-primary-green)';
        TrendIcon = TrendingUp;
        trendText = 'Rising';
    } else if (trendDir === 'down') {
        trendColor = '#EF5350';
        TrendIcon = TrendingDown;
        trendText = 'Falling';
    }

    return (
        <div className="voice-card">
            {/* Header */}
            <div className="voice-card-header">
                <span style={{ fontSize: '24px' }}>💰</span>
                <span className="voice-card-title">Mandi Price - {crop}</span>
            </div>

            {/* Price section */}
            <div style={{
                margin: '16px 0',
                padding: '16px',
                backgroundColor: 'rgba(255,255,255,0.6)',
                borderRadius: '8px',
                border: '1px solid var(--color-border)'
            }}>
                <div style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', marginBottom: '4px' }}>Current Price</div>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: 'var(--color-text-dark)' }}>{price} <span style={{ fontSize: '1rem', fontWeight: 'normal' }}>per quintal</span></div>
            </div>

            {/* Trend section */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                <div style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>Trend this week:</div>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    color: trendColor,
                    fontWeight: '600',
                    fontSize: '1rem'
                }}>
                    <TrendIcon size={20} />
                    <span>{trendText} {trendValue}</span>
                </div>
            </div>

            {/* Footer */}
            <div style={{
                borderTop: '1px solid var(--color-border)',
                paddingTop: '12px',
                fontSize: '0.8rem',
                color: 'var(--color-text-muted)'
            }}>
                Last updated: {lastUpdated}
            </div>
        </div>
    );
};

export default MarketPriceCard;
