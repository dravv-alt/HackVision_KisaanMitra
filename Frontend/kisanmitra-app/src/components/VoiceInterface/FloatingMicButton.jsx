import React from 'react';
import { Mic } from 'lucide-react';

const FloatingMicButton = ({ onClick }) => {
    return (
        <button
            onClick={onClick}
            style={{
                position: 'fixed',
                bottom: '32px',
                right: '32px',
                width: '72px',
                height: '72px',
                borderRadius: '50%',
                backgroundColor: 'var(--success-green)',
                border: 'none',
                boxShadow: '0 8px 24px rgba(0,0,0,0.2)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                cursor: 'pointer',
                zIndex: 1000,
                transition: 'transform 0.2s',
            }}
            onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.1)'}
            onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
            aria-label="Open Voice Assistant"
        >
            <Mic size={32} color="white" />
        </button>
    );
};

export default FloatingMicButton;
