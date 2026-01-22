import React from 'react';
import { MessageCircle } from 'lucide-react';
import './styles/voice-interface.css';

const TranscriptBox = ({ text }) => {
    return (
        <div style={{
            backgroundColor: 'rgba(255,255,255,0.5)',
            border: '1px dashed var(--color-border)',
            borderRadius: '12px',
            padding: '12px 16px',
            marginTop: '8px',
            display: 'flex',
            gap: '8px'
        }}>
            <MessageCircle size={16} color="var(--color-text-muted)" style={{ marginTop: '2px', flexShrink: 0 }} />
            <p style={{
                margin: 0,
                fontSize: '0.9rem',
                color: 'var(--color-text-secondary)',
                fontStyle: 'italic',
                lineHeight: '1.4'
            }}>
                "{text}"
            </p>
        </div>
    );
};

export default TranscriptBox;
