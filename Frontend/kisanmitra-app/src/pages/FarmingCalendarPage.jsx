import React from 'react';
import FarmingCalendar from '../components/Calendar/FarmingCalendar';
import { ChevronLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const FarmingCalendarPage = () => {
    const navigate = useNavigate();

    return (
        <div className="fade-in" style={{ paddingBottom: '80px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
                <button
                    onClick={() => navigate(-1)}
                    style={{
                        border: 'none',
                        background: 'transparent',
                        cursor: 'pointer',
                        padding: '8px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                    }}
                >
                    <ChevronLeft size={32} color="var(--color-text-dark)" />
                </button>
                <div>
                    <h2 style={{ fontSize: '2rem', fontWeight: '900', margin: '0 0 4px 0', color: 'var(--color-text-dark)' }}>Calendar & Tasks</h2>
                    <p style={{ fontSize: '1rem', color: 'var(--color-text-muted)', margin: 0 }}>Plan and track your farming activities.</p>
                </div>
            </div>

            <FarmingCalendar compact={false} />
        </div>
    );
};

export default FarmingCalendarPage;
