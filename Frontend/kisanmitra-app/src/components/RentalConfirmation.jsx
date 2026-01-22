import React, { useEffect, useState } from 'react';
import {
    Check,
    Calendar,
    Banknote,
    Mic
} from 'lucide-react';
import '../styles/global.css';

const RentalConfirmation = ({ bookingDetails, onFinalize, onClose }) => {
    // Animation state
    const [isConfirming, setIsConfirming] = useState(false);

    // Simulate voice confirmation effect on mount if needed, or trigger via button

    const handleConfirm = () => {
        setIsConfirming(true);
        // Simulate process
        setTimeout(() => {
            onFinalize();
        }, 2000);
    };

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0,0,0,0.5)',
            zIndex: 1000,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '16px'
        }}>
            <div
                className="card"
                style={{
                    width: '100%',
                    maxWidth: '400px',
                    backgroundColor: 'white',
                    padding: '0',
                    overflow: 'hidden',
                    display: 'flex',
                    flexDirection: 'column',
                    maxHeight: '90vh',
                    animation: 'slideUp 0.3s ease-out'
                }}
            >
                {/* Top decorative bar */}
                <div style={{ height: '80px', backgroundColor: 'var(--color-bg-beige)', width: '100%' }}></div>

                <div style={{ padding: '24px', flex: 1, overflowY: 'auto' }}>
                    <div style={{ textAlign: 'center', marginTop: '-50px', marginBottom: '16px' }}>
                        <div style={{
                            width: '64px',
                            height: '64px',
                            borderRadius: '16px',
                            backgroundColor: 'white',
                            display: 'inline-flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                            marginBottom: '16px'
                        }}>
                            <Check size={32} color="var(--color-primary-green)" strokeWidth={3} />
                        </div>
                        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', margin: '0 0 4px 0' }}>Rental Confirmation</h2>
                        <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>Please review your equipment request.</p>
                    </div>

                    <div style={{
                        backgroundColor: 'var(--color-bg-beige)',
                        borderRadius: '16px',
                        padding: '20px',
                        marginBottom: '24px',
                        border: '1px solid var(--color-border)'
                    }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', paddingBottom: '16px', borderBottom: '1px solid rgba(0,0,0,0.05)', marginBottom: '16px' }}>
                            <div style={{
                                width: '56px',
                                height: '56px',
                                borderRadius: '12px',
                                backgroundColor: 'white',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                overflow: 'hidden'
                            }}>
                                {/* Placeholder Icon */}
                                <span style={{ fontSize: '1.5rem' }}>🚜</span>
                            </div>
                            <div>
                                <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 'bold' }}>{bookingDetails.name || 'Equipment'}</h3>
                                <p style={{ margin: 0, fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>Model Details</p>
                            </div>
                        </div>

                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                            <div style={{ backgroundColor: 'white', padding: '12px', borderRadius: '12px', border: '1px solid rgba(0,0,0,0.05)' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--color-text-muted)', marginBottom: '4px', fontSize: '0.8rem', fontWeight: 'bold', textTransform: 'uppercase' }}>
                                    <Calendar size={14} /> DURATION
                                </div>
                                <p style={{ margin: 0, fontWeight: 'bold', fontSize: '1.1rem' }}>{bookingDetails.days || 2} Days</p>
                                <p style={{ margin: '4px 0 0 0', fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>Oct 24 - 26</p>
                            </div>
                            <div style={{ backgroundColor: 'white', padding: '12px', borderRadius: '12px', border: '1px solid rgba(0,0,0,0.05)' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--color-text-muted)', marginBottom: '4px', fontSize: '0.8rem', fontWeight: 'bold', textTransform: 'uppercase' }}>
                                    <Banknote size={14} /> TOTAL
                                </div>
                                <p style={{ margin: 0, fontWeight: 'bold', fontSize: '1.1rem' }}>₹{bookingDetails.totalCost || '0'}</p>
                                <p style={{ margin: '4px 0 0 0', fontSize: '0.75rem', color: 'var(--color-accent-ochre)', fontWeight: '600' }}>Pay on delivery</p>
                            </div>
                        </div>
                    </div>

                    {/* Voice Animation Area */}
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '24px', position: 'relative', height: '140px', justifyContent: 'center' }}>

                        {/* Simulated Pulse Ring */}
                        <div style={{
                            position: 'absolute',
                            width: '160px',
                            height: '160px',
                            borderRadius: '50%',
                            border: '1px solid rgba(76, 175, 80, 0.2)',
                            animation: 'ping 2s cubic-bezier(0, 0, 0.2, 1) infinite',
                            opacity: isConfirming ? 1 : 0.2
                        }}></div>
                        <div style={{
                            position: 'absolute',
                            width: '110px',
                            height: '110px',
                            borderRadius: '50%',
                            border: '1px solid rgba(76, 175, 80, 0.3)',
                            animation: 'ping 2s cubic-bezier(0, 0, 0.2, 1) infinite',
                            animationDelay: '0.4s',
                            opacity: isConfirming ? 1 : 0.2
                        }}></div>

                        <div style={{ zIndex: 10, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                            <button style={{
                                width: '72px',
                                height: '72px',
                                borderRadius: '50%',
                                backgroundColor: 'var(--color-primary-green)',
                                color: 'white',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                boxShadow: '0 8px 16px rgba(76, 175, 80, 0.3)',
                                marginBottom: '12px'
                            }}>
                                <Mic size={32} />
                            </button>
                            <p style={{ color: 'var(--color-primary-green)', fontWeight: 'bold' }}>
                                {isConfirming ? 'Confirming via voice...' : 'Say "Confirm Booking"'}
                            </p>
                        </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                        <button
                            onClick={onClose}
                            style={{
                                padding: '14px',
                                borderRadius: '12px',
                                border: '2px solid var(--color-border)',
                                background: 'transparent',
                                fontWeight: 'bold',
                                color: 'var(--color-text-muted)'
                            }}
                        >
                            Cancel
                        </button>
                        <button
                            onClick={handleConfirm}
                            disabled={isConfirming}
                            style={{
                                padding: '14px',
                                borderRadius: '12px',
                                backgroundColor: isConfirming ? '#A5D6A7' : 'var(--color-primary-green)',
                                color: 'white',
                                fontWeight: 'bold',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                gap: '8px'
                            }}
                        >
                            {isConfirming ? 'Confirming...' : (
                                <>
                                    Confirm <Check size={20} />
                                </>
                            )}
                        </button>
                    </div>
                </div>
            </div>
            <style>{`
        @keyframes ping {
            75%, 100% {
                transform: scale(1.5);
                opacity: 0;
            }
        }
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
      `}</style>
        </div>
    );
};

export default RentalConfirmation;
