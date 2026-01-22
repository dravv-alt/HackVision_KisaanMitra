import React from 'react';
import { Zap } from 'lucide-react';
import '../styles/voice-interface.css';

const ConfirmationCard = ({ question, details, onConfirm, onCancel }) => {
    return (
        <div className="voice-card" style={{
            backgroundColor: '#FFF9C4', // --warning-accent
            border: '2px solid #F9A825'
        }}>
            {/* Header */}
            <div className="voice-card-header" style={{ borderBottom: '1px solid rgba(0,0,0,0.1)' }}>
                <Zap size={24} color="#F57F17" fill="#F57F17" />
                <span className="voice-card-title" style={{ color: '#F57F17' }}>Action Required</span>
            </div>

            {/* Question */}
            <p style={{
                fontSize: '1.1rem',
                fontWeight: '600',
                color: 'var(--color-text-dark)',
                margin: '16px 0',
                lineHeight: '1.4'
            }}>
                {question}
            </p>

            {/* Details Box */}
            <div style={{
                backgroundColor: 'rgba(255,255,255,0.6)',
                padding: '12px',
                borderRadius: '8px',
                border: '1px solid rgba(0,0,0,0.1)',
                marginBottom: '20px'
            }}>
                {details.map((item, index) => (
                    <div key={index} style={{
                        display: 'flex',
                        gap: '8px',
                        marginBottom: '4px',
                        fontSize: '0.9rem',
                        color: 'var(--color-text-dark)'
                    }}>
                        <span>{item.icon}</span>
                        <span>{item.text}</span>
                    </div>
                ))}
            </div>

            {/* Actions */}
            <div style={{ display: 'flex', gap: '16px' }}>
                <button
                    onClick={onConfirm}
                    style={{
                        flex: 1,
                        height: '56px',
                        backgroundColor: 'var(--color-primary-green)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '12px',
                        fontSize: '1rem',
                        fontWeight: 'bold',
                        cursor: 'pointer',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        lineHeight: '1.2'
                    }}
                >
                    <span>Yes</span>
                    <span style={{ fontSize: '0.8rem', fontWeight: 'normal' }}>(हाँ)</span>
                </button>

                <button
                    onClick={onCancel}
                    style={{
                        flex: 1,
                        height: '56px',
                        backgroundColor: '#BDBDBD',
                        color: 'var(--color-text-dark)',
                        border: 'none',
                        borderRadius: '12px',
                        fontSize: '1rem',
                        fontWeight: 'bold',
                        cursor: 'pointer',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        lineHeight: '1.2'
                    }}
                >
                    <span>No</span>
                    <span style={{ fontSize: '0.8rem', fontWeight: 'normal' }}>(नहीं)</span>
                </button>
            </div>
        </div>
    );
};

export default ConfirmationCard;
