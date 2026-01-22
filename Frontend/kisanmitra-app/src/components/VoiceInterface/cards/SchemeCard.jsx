import React from 'react';
import { Volume2, ArrowRight, Eye } from 'lucide-react';
import '../styles/voice-interface.css';

const SchemeCard = ({ title, benefitAmount, description, isTopRecommendation }) => {
    return (
        <div className="voice-card animate-fade-in" style={{
            backgroundColor: '#E8F0EA', // Sage Light from design
            border: '1px solid #C5DBC6',
            boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
        }}>
            {/* Header / Badge */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                <div>
                    {isTopRecommendation && (
                        <div style={{
                            backgroundColor: 'var(--color-primary-green)', color: 'white',
                            fontSize: '0.75rem', fontWeight: 'bold', padding: '2px 8px',
                            borderRadius: '12px', width: 'fit-content', marginBottom: '6px',
                            textTransform: 'uppercase', letterSpacing: '0.5px'
                        }}>
                            Top Recommendation
                        </div>
                    )}
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--color-primary-green)', fontSize: '0.9rem', fontWeight: 'bold' }}>
                        <Volume2 size={16} /> Reading summary...
                    </div>
                </div>

                {/* Benefit Amount (Right Side) */}
                <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--color-text-secondary)', textTransform: 'uppercase' }}>Benefit Amount</div>
                    <div style={{ fontSize: '1.25rem', fontWeight: '900', color: 'var(--color-text-dark)' }}>{benefitAmount}</div>
                </div>
            </div>

            {/* Title */}
            <h3 style={{ fontSize: '1.5rem', fontWeight: '900', color: 'var(--color-text-dark)', marginBottom: '16px', lineHeight: 1.2 }}>{title}</h3>

            {/* Description Box */}
            <div style={{
                backgroundColor: 'rgba(255,255,255,0.6)',
                borderRadius: '12px',
                padding: '16px',
                marginBottom: '20px',
                border: '1px solid rgba(255,255,255,0.5)',
                fontSize: '1rem',
                color: 'var(--color-text-dark)',
                lineHeight: 1.6
            }}>
                "{description}"
            </div>

            {/* Actions */}
            <div style={{ display: 'flex', gap: '12px' }}>
                <button className="voice-card-cta" style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                    Check Eligibility <ArrowRight size={18} />
                </button>
                <button style={{
                    flex: 1,
                    backgroundColor: 'transparent',
                    border: '2px solid var(--color-primary-green)',
                    color: 'var(--color-primary-green)',
                    padding: '12px',
                    borderRadius: '12px',
                    fontWeight: 'bold',
                    cursor: 'pointer',
                    display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px'
                }}>
                    View Details <Eye size={18} />
                </button>
            </div>
        </div>
    );
};

export default SchemeCard;
