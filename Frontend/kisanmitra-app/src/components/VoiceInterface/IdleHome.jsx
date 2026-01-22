import React from 'react';
import { Mic, IndianRupee, Sprout, Bug, Landmark } from 'lucide-react';

const IdleHome = ({ onMicClick }) => {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', padding: '24px' }}>

            {/* Mic Section */}
            <div style={{ marginBottom: '32px', position: 'relative' }}>
                <div
                    className="mic-btn-large"
                    onClick={onMicClick}
                >
                    <Mic size={48} color="white" />
                </div>
            </div>

            <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: 'var(--text-primary)', marginBottom: '8px', textAlign: 'center' }}>
                Bolo, main sun raha hoon
            </h2>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '48px', textAlign: 'center' }}>
                (Speak, I am listening)
            </p>

            {/* Chips Grid */}
            <div style={{ width: '100%', maxWidth: '400px' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--text-secondary)', marginBottom: '16px', letterSpacing: '1px' }}>
                    TRY ASKING ABOUT
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '12px' }}>
                    <Chip icon={IndianRupee} text="Mandi prices?" />
                    <Chip icon={Sprout} text="Crop advice?" />
                    <Chip icon={Bug} text="Check crop disease?" />
                    <Chip icon={Landmark} text="Schemes?" />
                </div>
            </div>
        </div>
    );
};

const Chip = ({ icon: Icon, text }) => (
    <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
        padding: '16px',
        backgroundColor: 'var(--card-bg)',
        borderRadius: 'var(--radius-md)',
        border: '1px solid var(--card-border)',
        cursor: 'pointer',
        transition: 'transform 0.2s'
    }}
        onMouseEnter={e => e.currentTarget.style.transform = 'translateY(-2px)'}
        onMouseLeave={e => e.currentTarget.style.transform = 'translateY(0)'}
    >
        <Icon size={24} color="var(--text-primary)" />
        <span style={{ fontSize: '1rem', fontWeight: '500', color: 'var(--text-primary)' }}>{text}</span>
    </div>
);

export default IdleHome;
