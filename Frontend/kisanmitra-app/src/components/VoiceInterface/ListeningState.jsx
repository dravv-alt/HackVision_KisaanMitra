import React from 'react';
import { Mic, Square } from 'lucide-react';

const ListeningState = ({ onCancel, isRecording, onStop }) => {
    return (
        <div className="listening-state" style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100%',
            padding: '40px'
        }}>
            {/* Animated Microphone Circle */}
            <div style={{ position: 'relative', marginBottom: '32px' }}>
                {/* Pulsing rings */}
                <div className="pulse-ring" style={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: '200px',
                    height: '200px',
                    borderRadius: '50%',
                    border: '4px solid rgba(217, 76, 76, 0.3)',
                    animation: 'pulse-ring 2s infinite'
                }}></div>
                <div className="pulse-ring" style={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: '200px',
                    height: '200px',
                    borderRadius: '50%',
                    border: '4px solid rgba(217, 76, 76, 0.3)',
                    animation: 'pulse-ring 2s 1s infinite'
                }}></div>

                {/* Microphone Icon */}
                <div style={{
                    width: '120px',
                    height: '120px',
                    borderRadius: '50%',
                    backgroundColor: isRecording ? '#D32F2F' : 'var(--color-primary-green)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    boxShadow: '0 8px 30px rgba(211, 47, 47, 0.4)',
                    position: 'relative',
                    zIndex: 10,
                    animation: isRecording ? 'pulse-mic 1.5s infinite' : 'none'
                }}>
                    <Mic size={56} color="white" />
                </div>
            </div>

            {/* Status Text */}
            <h3 style={{
                fontSize: '1.5rem',
                fontWeight: 'bold',
                color: 'var(--color-text-dark)',
                marginBottom: '8px'
            }}>
                {isRecording ? '🔴 Recording...' : 'Listening...'}
            </h3>
            <p style={{
                fontSize: '1rem',
                color: 'var(--color-text-muted)',
                marginBottom: '32px',
                textAlign: 'center'
            }}>
                {isRecording ? 'Speak in Hindi or English' : 'Preparing microphone...'}
            </p>

            {/* Audio Waveform Simulation */}
            {isRecording && (
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    height: '40px',
                    marginBottom: '32px'
                }}>
                    {[...Array(20)].map((_, i) => (
                        <div
                            key={i}
                            style={{
                                width: '3px',
                                backgroundColor: 'var(--color-primary-green)',
                                borderRadius: '2px',
                                animation: `wave ${0.5 + Math.random()}s infinite ease-in-out`,
                                animationDelay: `${i * 0.05}s`
                            }}
                        ></div>
                    ))}
                </div>
            )}

            {/* Action Buttons */}
            <div style={{ display: 'flex', gap: '16px' }}>
                {isRecording ? (
                    <>
                        <button
                            onClick={onStop}
                            style={{
                                padding: '14px 32px',
                                backgroundColor: '#D32F2F',
                                color: 'white',
                                borderRadius: '12px',
                                fontSize: '1rem',
                                fontWeight: 'bold',
                                border: 'none',
                                cursor: 'pointer',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px',
                                boxShadow: '0 4px 14px rgba(211, 47, 47, 0.4)'
                            }}
                        >
                            <Square size={20} /> Stop Recording
                        </button>
                        <button
                            onClick={onCancel}
                            style={{
                                padding: '14px 32px',
                                backgroundColor: 'transparent',
                                color: 'var(--color-text-muted)',
                                borderRadius: '12px',
                                fontSize: '1rem',
                                fontWeight: 'bold',
                                border: '2px solid var(--color-border)',
                                cursor: 'pointer'
                            }}
                        >
                            Cancel
                        </button>
                    </>
                ) : (
                    <button
                        onClick={onCancel}
                        style={{
                            padding: '14px 32px',
                            backgroundColor: 'transparent',
                            color: 'var(--color-text-muted)',
                            borderRadius: '12px',
                            fontSize: '1rem',
                            fontWeight: 'bold',
                            border: '2px solid var(--color-border)',
                            cursor: 'pointer'
                        }}
                    >
                        Cancel
                    </button>
                )}
            </div>
        </div>
    );
};

export default ListeningState;
