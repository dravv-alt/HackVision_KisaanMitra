import React from 'react';
import { Mic } from 'lucide-react';

const ListeningState = ({ onCancel }) => {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', padding: '24px', backgroundColor: 'rgba(0,0,0,0.02)' }}>

            {/* Active Mic */}
            <div style={{ marginBottom: '32px', position: 'relative' }}>
                <div className="mic-btn-active" style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    borderRadius: '50%',
                    position: 'relative'
                }}>
                    {/* Audio Wave Simulation */}
                    <div style={{ display: 'flex', gap: '4px', alignItems: 'center', height: '32px' }}>
                        {[1, 2, 3, 4, 5].map(i => (
                            <div key={i} style={{
                                width: '4px',
                                backgroundColor: 'white',
                                borderRadius: '2px',
                                animation: `audio-wave 0.8s ease-in-out infinite`,
                                animationDelay: `${i * 0.1}s`,
                                height: '100%'
                            }} />
                        ))}
                    </div>
                </div>
            </div>

            <h2 style={{ fontSize: '1.5rem', fontWeight: '500', color: 'var(--success-green)', marginBottom: '8px', textAlign: 'center' }}>
                Sun raha hoon...
            </h2>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '48px', textAlign: 'center' }}>
                (Listening to you...)
            </p>

            <button
                onClick={onCancel}
                style={{
                    padding: '12px 48px',
                    borderRadius: '24px',
                    backgroundColor: 'var(--neutral-gray)',
                    border: 'none',
                    color: 'var(--text-primary)',
                    fontSize: '1rem',
                    fontWeight: '500',
                    cursor: 'pointer'
                }}
            >
                Cancel
            </button>
        </div>
    );
};

export default ListeningState;
