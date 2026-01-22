import React, { useState, useEffect } from 'react';
import { Play, Pause, Volume2 } from 'lucide-react';
import './styles/voice-interface.css';

const AudioPlayer = ({ transcript, duration = 15 }) => {
    const [isPlaying, setIsPlaying] = useState(true);
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        let interval;
        if (isPlaying) {
            interval = setInterval(() => {
                setProgress((prev) => {
                    if (prev >= 100) {
                        setIsPlaying(false);
                        return 0;
                    }
                    return prev + (100 / (duration * 10)); // updates every 100ms
                });
            }, 100);
        }
        return () => clearInterval(interval);
    }, [isPlaying, duration]);

    const togglePlay = () => setIsPlaying(!isPlaying);

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    };

    const currentTime = (progress / 100) * duration;

    return (
        <div style={{
            padding: '12px 16px',
            backgroundColor: 'rgba(255,255,255,0.4)',
            borderRadius: '12px',
            marginTop: '12px',
            marginBottom: '12px',
            border: '1px solid rgba(0,0,0,0.05)'
        }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--color-primary-green)', fontWeight: '600', fontSize: '0.9rem' }}>
                    <Volume2 size={16} />
                    <span>{isPlaying ? 'Playing response...' : 'Audio paused'}</span>
                </div>
                <button
                    onClick={togglePlay}
                    style={{
                        background: 'none',
                        border: 'none',
                        cursor: 'pointer',
                        color: 'var(--color-primary-green)',
                        padding: 0
                    }}
                >
                    {isPlaying ? <Pause size={20} fill="currentColor" /> : <Play size={20} fill="currentColor" />}
                </button>
            </div>

            {/* Progress Bar Container */}
            <div style={{
                height: '4px',
                backgroundColor: 'rgba(0,0,0,0.1)',
                borderRadius: '2px',
                width: '100%',
                position: 'relative'
            }}>
                {/* Progress Fill */}
                <div style={{
                    width: `${progress}%`,
                    height: '100%',
                    backgroundColor: 'var(--color-primary-green)',
                    borderRadius: '2px',
                    transition: 'width 0.1s linear'
                }}></div>
                {/* Handle */}
                <div style={{
                    position: 'absolute',
                    left: `${progress}%`,
                    top: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: '12px',
                    height: '12px',
                    backgroundColor: 'var(--color-primary-green)',
                    borderRadius: '50%',
                    transition: 'left 0.1s linear'
                }}></div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '4px' }}>
                <span>{formatTime(currentTime)}</span>
                <span>{formatTime(duration)}</span>
            </div>

            {/* Transcript (Standardized place for it usually, but can be separate) */}
            {/* Keeping it separate as per design prompt 'Transcript Section' */}
        </div>
    );
};

export default AudioPlayer;
