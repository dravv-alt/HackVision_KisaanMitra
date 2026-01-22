import React from 'react';
import { TrendingDown, PieChart } from 'lucide-react';
import '../styles/voice-interface.css';

const FinanceCard = ({ month, totalExpense, categories }) => {
    return (
        <div className="voice-card">
            {/* Header */}
            <div className="voice-card-header">
                <span style={{ fontSize: '24px' }}>📊</span>
                <span className="voice-card-title">Expense Report - {month}</span>
            </div>

            {/* Total Expense */}
            <div style={{
                margin: '16px 0',
                padding: '16px',
                backgroundColor: 'rgba(217, 114, 76, 0.1)', // Light Red Tint
                borderRadius: '12px',
                border: '1px solid rgba(217, 114, 76, 0.3)',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
            }}>
                <div>
                    <div style={{ fontSize: '0.85rem', color: '#6B6358', marginBottom: '4px', fontWeight: 'bold' }}>TOTAL SPENT</div>
                    <div style={{ fontSize: '1.75rem', fontWeight: '900', color: '#D9724C' }}>{totalExpense}</div>
                </div>
                <div style={{
                    padding: '8px',
                    borderRadius: '50%',
                    backgroundColor: 'rgba(255,255,255,0.5)',
                    color: '#D9724C'
                }}>
                    <TrendingDown size={24} />
                </div>
            </div>

            {/* Breakdown */}
            <div style={{ marginBottom: '8px' }}>
                <div style={{ fontSize: '0.9rem', color: '#6B6358', fontWeight: 'bold', marginBottom: '8px' }}>Top Categories</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {categories.map((cat, idx) => (
                        <div key={idx} style={{
                            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                            padding: '8px 12px', backgroundColor: '#FDFCF6', borderRadius: '8px',
                            border: '1px solid #E6DCC8'
                        }}>
                            <span style={{ fontSize: '0.9rem', color: '#423E37' }}>{cat.name}</span>
                            <span style={{ fontSize: '0.9rem', fontWeight: 'bold', color: '#423E37' }}>{cat.amount}</span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Footer Action */}
            <div style={{
                marginTop: '16px',
                paddingTop: '12px',
                borderTop: '1px solid #E6DCC8',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                color: '#8FA892', // Primary
                fontWeight: 'bold',
                fontSize: '0.9rem',
                cursor: 'pointer'
            }}>
                <PieChart size={16} /> View Full Analysis
            </div>
        </div>
    );
};

export default FinanceCard;
