import React from 'react';
import { Brain } from 'lucide-react';
import './styles/voice-interface.css';

const ContextIndicator = ({ contextItems }) => {
    return (
        <div style={{
            backgroundColor: 'rgba(255, 249, 196, 0.3)',
            border: '1px solid #FFF9C4', // Warning accent
            borderRadius: '12px',
            padding: '12px 16px',
            marginBottom: '12px',
            width: 'fit-content',
            maxWidth: '85%'
        }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <Brain size={16} color="var(--color-text-secondary)" />
                <span style={{ fontSize: '0.8rem', fontWeight: '600', color: 'var(--color-text-secondary)', textTransform: 'uppercase' }}>
                    Context Used
                </span>
            </div>

            <ul style={{ margin: 0, paddingLeft: '20px', color: 'var(--color-text-secondary)', fontSize: '0.85rem' }}>
                {contextItems.map((item, index) => (
                    <li key={index} style={{ marginBottom: '2px' }}>{item}</li>
                ))}
            </ul>
        </div>
    );
};

export default ContextIndicator;
