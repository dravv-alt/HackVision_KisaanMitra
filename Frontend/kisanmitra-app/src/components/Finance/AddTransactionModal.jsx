import React, { useState } from 'react';
import { X, Check, IndianRupee, Calendar, Tag, FileText } from 'lucide-react';

const COLORS = {
    primary: "#8FA892",
    primaryDark: "#758E78",
    accentOchre: "#D9A54C",
    textMain: "#423E37",
    textSec: "#6B6358",
    bgLight: "#FDFCF6",
    cardBeige: "#F2EFE5",
};

const AddTransactionModal = ({ isOpen, onClose, onSave }) => {
    const [formData, setFormData] = useState({
        type: 'expense', // or 'income'
        title: '',
        amount: '',
        category: 'Seeds',
        date: new Date().toISOString().split('T')[0],
        description: ''
    });

    if (!isOpen) return null;

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSave({
            ...formData,
            id: Date.now(),
            dateFormatted: new Date(formData.date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })
        });
        onClose();
        // Reset form slightly delayed or just rely on unmount/remount if managed by parent
        setFormData({
            type: 'expense',
            title: '',
            amount: '',
            category: 'Seeds',
            date: new Date().toISOString().split('T')[0],
            description: ''
        });
    };

    return (
        <div style={{
            position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center',
            zIndex: 1000, backdropFilter: 'blur(4px)'
        }}>
            <div className="fade-in" style={{
                backgroundColor: 'white', borderRadius: '24px', padding: '32px',
                width: '100%', maxWidth: '500px',
                boxShadow: '0 20px 50px rgba(0,0,0,0.2)'
            }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                    <h3 style={{ margin: 0, fontSize: '1.5rem', fontWeight: '900', color: COLORS.textMain }}>Add Transaction</h3>
                    <button onClick={onClose} style={{
                        background: 'none', border: 'none', cursor: 'pointer',
                        padding: '8px', borderRadius: '50%', backgroundColor: COLORS.bgLight
                    }}>
                        <X size={24} color={COLORS.textSec} />
                    </button>
                </div>

                <form onSubmit={handleSubmit}>
                    {/* Type Toggle */}
                    <div style={{ display: 'flex', gap: '12px', marginBottom: '24px' }}>
                        <button
                            type="button"
                            onClick={() => setFormData({ ...formData, type: 'expense' })}
                            style={{
                                flex: 1, padding: '12px', borderRadius: '12px', border: 'none',
                                backgroundColor: formData.type === 'expense' ? '#FFEBEE' : COLORS.bgLight,
                                color: formData.type === 'expense' ? '#C62828' : COLORS.textSec,
                                fontWeight: 'bold', cursor: 'pointer', transition: 'all 0.2s'
                            }}
                        >
                            Expense (Out)
                        </button>
                        <button
                            type="button"
                            onClick={() => setFormData({ ...formData, type: 'income' })}
                            style={{
                                flex: 1, padding: '12px', borderRadius: '12px', border: 'none',
                                backgroundColor: formData.type === 'income' ? '#E8F5E9' : COLORS.bgLight,
                                color: formData.type === 'income' ? '#2E7D32' : COLORS.textSec,
                                fontWeight: 'bold', cursor: 'pointer', transition: 'all 0.2s'
                            }}
                        >
                            Income (In)
                        </button>
                    </div>

                    {/* Inputs */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        <div style={{ position: 'relative' }}>
                            <Tag size={18} color={COLORS.textSec} style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)' }} />
                            <input
                                type="text"
                                name="title"
                                placeholder="What is this for? (e.g. Wheat Seeds)"
                                value={formData.title}
                                onChange={handleChange}
                                required
                                style={{
                                    width: '100%', padding: '14px 14px 14px 48px', borderRadius: '12px',
                                    border: `1px solid ${COLORS.textSec}40`, fontSize: '1rem', outline: 'none',
                                    backgroundColor: COLORS.bgLight
                                }}
                            />
                        </div>

                        <div style={{ position: 'relative' }}>
                            <IndianRupee size={18} color={COLORS.textSec} style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)' }} />
                            <input
                                type="number"
                                name="amount"
                                placeholder="Amount"
                                value={formData.amount}
                                onChange={handleChange}
                                required
                                style={{
                                    width: '100%', padding: '14px 14px 14px 48px', borderRadius: '12px',
                                    border: `1px solid ${COLORS.textSec}40`, fontSize: '1rem', outline: 'none',
                                    backgroundColor: COLORS.bgLight
                                }}
                            />
                        </div>

                        <div style={{ display: 'flex', gap: '16px' }}>
                            <div style={{ position: 'relative', flex: 1 }}>
                                <Calendar size={18} color={COLORS.textSec} style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)' }} />
                                <input
                                    type="date"
                                    name="date"
                                    value={formData.date}
                                    onChange={handleChange}
                                    style={{
                                        width: '100%', padding: '14px 14px 14px 48px', borderRadius: '12px',
                                        border: `1px solid ${COLORS.textSec}40`, fontSize: '1rem', outline: 'none',
                                        backgroundColor: COLORS.bgLight
                                    }}
                                />
                            </div>
                            <select
                                name="category"
                                value={formData.category}
                                onChange={handleChange}
                                style={{
                                    flex: 1, padding: '14px', borderRadius: '12px',
                                    border: `1px solid ${COLORS.textSec}40`, fontSize: '1rem', outline: 'none',
                                    backgroundColor: COLORS.bgLight
                                }}
                            >
                                <option>Seeds</option>
                                <option>Fertilizers</option>
                                <option>Labor</option>
                                <option>Machinery</option>
                                <option>Harvest</option>
                                <option>Other</option>
                            </select>
                        </div>
                    </div>

                    <button type="submit" style={{
                        width: '100%', padding: '16px', borderRadius: '16px',
                        backgroundColor: COLORS.primary, color: 'white', fontSize: '1.1rem',
                        fontWeight: 'bold', border: 'none', marginTop: '32px', cursor: 'pointer',
                        display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px'
                    }}>
                        <Check size={20} /> Save Transaction
                    </button>
                </form>
            </div>
        </div>
    );
};

export default AddTransactionModal;
