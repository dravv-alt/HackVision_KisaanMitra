import React, { useState, useEffect } from 'react';
import {
    ArrowLeft, Calendar, Plus, TrendingUp, Info,
    CheckCircle, AlertCircle, PieChart, Receipt,
    ChevronRight, Download, Filter, Mic,
    Droplets, Lightbulb, Wallet, ArrowUpRight, ArrowDownRight,
    Leaf, CloudRain, Tractor, Users
} from 'lucide-react';

import '../styles/global.css';
import AddTransactionModal from '../components/Finance/AddTransactionModal';

// --- Colors from Design ---
const COLORS = {
    primary: "#8FA892",
    primaryDark: "#758E78",
    accentOchre: "#D9A54C",
    accentAlert: "#D9724C",
    textMain: "#423E37",
    textSec: "#6B6358",
    bgLight: "#FDFCF6",
    cardBeige: "#F2EFE5",
};

const FARMER_ID = "FARMER001";

const Finance = () => {
    // Navigation State: 'overview', 'crop-profit', 'expenses', 'insights'
    const [view, setView] = useState('overview');
    const [loading, setLoading] = useState(true);

    // --- Data State ---
    const [financeData, setFinanceData] = useState({
        totals: { totalIncome: 0, totalExpense: 0, profitOrLoss: 0, profitMarginPct: 0 },
        crop_performance: [],
        recent_transactions: [],
        insights: { suggestions: [], lossCauses: [] }
    });

    const [isModalOpen, setIsModalOpen] = useState(false);

    // --- Fetch Data ---
    useEffect(() => {
        fetchFinanceDashboard();
    }, []);

    const fetchFinanceDashboard = async () => {
        try {
            setLoading(true);
            const res = await fetch(`/api/v1/finance/${FARMER_ID}/dashboard`);
            const data = await res.json();

            if (data) {
                setFinanceData(data);
            }
            setLoading(false);
        } catch (error) {
            console.error("Failed to fetch finance data:", error);
            setLoading(false);
        }
    };

    const handleAddTransaction = async (newTx) => {
        // Prepare API Payload
        const payload = {
            season: "KHARIF",
            category: newTx.category,
            amount: parseFloat(newTx.amount),
            notes: newTx.title,
            type: newTx.type, // 'expense' or 'income'
            relatedCropId: null // Default generic
        };

        try {
            const res = await fetch(`/api/v1/finance/${FARMER_ID}/transaction`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const result = await res.json();

            if (result.success) {
                // Refresh Dashboard to show new numbers
                fetchFinanceDashboard();
            } else {
                alert("Failed to add transaction");
            }
        } catch (error) {
            console.error("Error adding transaction:", error);
        }
    };

    // Formatting Helper
    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumSignificantDigits: 10
        }).format(amount || 0);
    };

    const { totals, crop_performance, recent_transactions, insights } = financeData;

    // --- VIEW: DASHBOARD (Screen 1) ---
    const renderOverview = () => (
        <div className="fade-in">
            {/* Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: '32px' }}>
                <div>
                    <h2 style={{ fontSize: '2.5rem', fontWeight: '900', color: COLORS.textMain, margin: 0, lineHeight: 1.2 }}>Financial Tracking</h2>
                    <p style={{ fontSize: '1.1rem', color: COLORS.textSec, marginTop: '8px' }}>Overview of your farm's financial health</p>
                </div>
                <div style={{ display: 'flex', gap: '12px' }}>
                    <button onClick={() => setView('insights')} style={{
                        display: 'flex', alignItems: 'center', gap: '8px',
                        padding: '12px 20px', borderRadius: '12px',
                        backgroundColor: COLORS.cardBeige, color: COLORS.textMain,
                        border: `1px solid ${COLORS.accentOchre}40`, fontWeight: 'bold', cursor: 'pointer'
                    }}>
                        <Lightbulb size={20} color={COLORS.accentOchre} /> AI Insights
                    </button>
                    <button onClick={() => setIsModalOpen(true)} style={{
                        display: 'flex', alignItems: 'center', gap: '8px',
                        padding: '12px 20px', borderRadius: '12px',
                        backgroundColor: COLORS.primary, color: 'white',
                        border: 'none', fontWeight: 'bold', boxShadow: '0 4px 14px rgba(143, 168, 146, 0.4)',
                        cursor: 'pointer'
                    }}>
                        <Plus size={20} /> Add Transaction
                    </button>
                </div>
            </div>

            {/* Summary Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px', marginBottom: '32px' }}>
                <SummaryCard
                    title="Total Income"
                    amount={formatCurrency(totals.totalIncome)}
                    trend={"+12% from last season"}
                    trendColor={COLORS.primaryDark}
                    icon={Wallet}
                    iconColor={COLORS.primary}
                    bgColor="rgba(143, 168, 146, 0.1)"
                />
                <SummaryCard
                    title="Total Expenses"
                    amount={formatCurrency(totals.totalExpense)}
                    trend="Mostly seeds & fertilizer"
                    trendColor={COLORS.textSec}
                    icon={ArrowDownRight}
                    iconColor={COLORS.accentAlert}
                    bgColor="rgba(217, 114, 76, 0.1)"
                />
                <SummaryCard
                    title="Net Profit"
                    amount={formatCurrency(totals.profitOrLoss)}
                    trend={`${totals.profitMarginPct}% Margin`}
                    trendColor={totals.profitOrLoss >= 0 ? COLORS.primaryDark : COLORS.accentAlert}
                    icon={CheckCircle}
                    iconColor={COLORS.accentOchre}
                    bgColor="rgba(217, 165, 76, 0.1)"
                />
            </div>

            {/* Main Action Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '32px', marginBottom: '40px' }}>
                {/* Visual Chart Placeholder reused from design */}
                <div style={{
                    backgroundColor: 'white', borderRadius: '24px', padding: '32px',
                    border: '1px solid #E6DCC8', display: 'flex', flexDirection: 'column',
                    gridColumn: 'span 1'
                }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
                        <div>
                            <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: COLORS.textMain, display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <TrendingUp size={24} /> Cash Flow
                            </h3>
                            <p style={{ color: COLORS.textSec }}>Money In vs Out</p>
                        </div>
                    </div>
                    {/* Simplified Visual Bars */}
                    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-end', gap: '40px', height: '180px', borderBottom: '1px dashed #E6DCC8' }}>
                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                            <div style={{ height: '140px', width: '60px', backgroundColor: COLORS.primary, borderRadius: '8px 8px 0 0' }}></div>
                            <span style={{ fontWeight: 'bold', color: COLORS.primaryDark }}>Inflow</span>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                            <div style={{ height: '60px', width: '60px', backgroundColor: COLORS.accentAlert, borderRadius: '8px 8px 0 0' }}></div>
                            <span style={{ fontWeight: 'bold', color: COLORS.accentAlert }}>Outflow</span>
                        </div>
                    </div>
                    <p style={{ textAlign: 'center', marginTop: '16px', color: COLORS.textSec, fontStyle: 'italic' }}>
                        Net Profit Margin is currently <strong style={{ color: COLORS.primaryDark }}>{totals.profitMarginPct}%</strong>.
                    </p>
                </div>

                {/* Navigation Buttons List */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <NavBigButton
                        title="Crop-wise Profit"
                        desc="See which crop is making you the most money."
                        icon={PieChart}
                        iconColor={COLORS.accentOchre}
                        onClick={() => setView('crop-profit')}
                    />
                    <NavBigButton
                        title="View Expenses"
                        desc="Check bills for seeds, fertilizers, and labor."
                        icon={Receipt}
                        iconColor={COLORS.primary}
                        onClick={() => setView('expenses')}
                    />
                </div>
            </div>
        </div>
    );

    // --- VIEW: CROP PROFIT (Screen 2) ---
    const renderCropProfit = () => (
        <div className="fade-in">
            {/* Nav Header */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '32px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <button onClick={() => setView('overview')} className="icon-btn-refined" style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
                        <ArrowLeft size={24} color={COLORS.textMain} />
                    </button>
                    <div>
                        <h2 style={{ fontSize: '2rem', fontWeight: '900', color: COLORS.textMain, margin: '0' }}>Crop-Wise Performance</h2>
                        <p style={{ color: COLORS.textSec }}>Financial Year 2023-24</p>
                    </div>
                </div>
                <button className="btn-secondary" style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 20px', borderRadius: '12px', border: '1px solid #ccc', background: 'white', cursor: 'pointer' }}>
                    <Download size={18} /> Export Report
                </button>
            </div>

            {/* List */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                {crop_performance.map((crop) => (
                    <div key={crop.id} className="hover-scale" style={{
                        backgroundColor: 'white', borderRadius: '16px', padding: '24px',
                        border: '1px solid #E6DCC8', boxShadow: '0 2px 8px rgba(0,0,0,0.02)'
                    }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '24px' }}>
                            <div style={{ display: 'flex', gap: '16px' }}>
                                <div style={{
                                    width: '56px', height: '56px', borderRadius: '12px',
                                    backgroundColor: COLORS.bgLight, border: '1px solid #E6DCC8',
                                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                                    color: COLORS.accentOchre
                                }}>
                                    <Leaf size={32} />
                                </div>
                                <div>
                                    <h3 style={{ fontSize: '1.25rem', fontWeight: '900', color: COLORS.textMain, margin: 0 }}>{crop.name}</h3>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: COLORS.textSec, fontSize: '0.9rem', marginTop: '4px' }}>
                                        <TrendingUp size={16} /> {crop.area}
                                    </div>
                                </div>
                            </div>
                            <span style={{
                                padding: '6px 12px', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 'bold',
                                backgroundColor: crop.trend === 'up' ? '#E8F5E9' : '#FFF8E1',
                                color: crop.trend === 'up' ? '#2E7D32' : COLORS.accentOchre,
                                display: 'flex', alignItems: 'center', gap: '6px'
                            }}>
                                <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'currentColor' }} />
                                {crop.status}
                            </span>
                        </div>

                        {/* Grid Stats */}
                        <div style={{
                            display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)',
                            backgroundColor: COLORS.cardBeige, borderRadius: '12px', padding: '16px',
                            border: '1px solid #E6DCC8'
                        }}>
                            <div>
                                <div style={{ fontSize: '0.75rem', fontWeight: 'bold', color: COLORS.textSec, textTransform: 'uppercase' }}>Income</div>
                                <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: COLORS.textMain }}>{formatCurrency(crop.income)}</div>
                            </div>
                            <div style={{ borderLeft: '1px solid rgba(0,0,0,0.1)', paddingLeft: '16px' }}>
                                <div style={{ fontSize: '0.75rem', fontWeight: 'bold', color: COLORS.textSec, textTransform: 'uppercase' }}>Total Expense</div>
                                <div style={{ fontSize: '1.25rem', fontWeight: 'bold', color: COLORS.textMain }}>{formatCurrency(crop.expense)}</div>
                            </div>
                            <div style={{ borderLeft: '1px solid rgba(0,0,0,0.1)', paddingLeft: '16px' }}>
                                <div style={{ fontSize: '0.75rem', fontWeight: 'bold', color: COLORS.textSec, textTransform: 'uppercase' }}>Net Profit</div>
                                <div style={{ fontSize: '1.5rem', fontWeight: '900', color: crop.trend === 'up' ? COLORS.primaryDark : COLORS.accentOchre }}>{formatCurrency(crop.profit)}</div>
                            </div>
                        </div>

                        <div style={{ textAlign: 'right', marginTop: '16px' }}>
                            <button onClick={() => setView('expenses')} style={{ fontSize: '0.9rem', fontWeight: 'bold', color: COLORS.primary, background: 'none', border: 'none', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                                View Expense Details <ArrowRight size={16} />
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );

    // --- VIEW: EXPENSES (Screen 3) ---
    const renderExpenses = () => (
        <div className="fade-in">
            {/* Nav Header */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '32px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <button onClick={() => setView('overview')} className="icon-btn-refined" style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
                        <ArrowLeft size={24} color={COLORS.textMain} />
                    </button>
                    <div>
                        <h2 style={{ fontSize: '2rem', fontWeight: '900', color: COLORS.textMain, margin: '0' }}>Financial Tracking</h2>
                        <p style={{ color: COLORS.textSec }}>Track every rupee spent</p>
                    </div>
                </div>
                <div style={{ padding: '8px 16px', backgroundColor: COLORS.cardBeige, borderRadius: '12px', border: `1px solid ${COLORS.accentAlert}40` }}>
                    <span style={{ fontSize: '0.85rem', fontWeight: 'bold', color: COLORS.textSec, textTransform: 'uppercase' }}>Total Expenses</span>
                    <div style={{ fontSize: '1.5rem', fontWeight: '900', color: COLORS.textMain }}>{formatCurrency(totals.totalExpense)}</div>
                </div>
            </div>

            {/* Categories */}
            <div style={{ marginBottom: '40px' }}>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: COLORS.textMain, marginBottom: '16px' }}>Categories</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '16px' }}>
                    <ExpenseCategory title="Seeds" amount={formatCurrency(totals.totalExpense * 0.2)} color="green" icon={Leaf} />
                    <ExpenseCategory title="Fertilizers" amount={formatCurrency(totals.totalExpense * 0.4)} color="blue" icon={Droplets} />
                    <ExpenseCategory title="Labor" amount={formatCurrency(totals.totalExpense * 0.3)} color="orange" icon={Users} />
                    <ExpenseCategory title="Machinery" amount={formatCurrency(totals.totalExpense * 0.1)} color="red" icon={Tractor} />
                </div>
            </div>

            {/* Transactions List */}
            <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: COLORS.textMain }}>Recent Transactions</h3>
                    <button style={{ color: COLORS.primary, fontWeight: 'bold', background: 'none', border: 'none', cursor: 'pointer' }}>View All</button>
                </div>
                <div style={{ backgroundColor: 'white', borderRadius: '16px', border: '1px solid #E6DCC8', overflow: 'hidden' }}>
                    {recent_transactions.length > 0 ? recent_transactions.map((tx) => (
                        <TransactionRow
                            key={tx.id}
                            title={tx.title}
                            date={tx.date}
                            amount={tx.amount}
                            iconColor={tx.iconColor}
                            icon={Leaf} // Simplified, can be dynamic
                        />
                    )) : (
                        <div style={{ padding: '20px', textAlign: 'center', color: COLORS.textSec }}>No transactions yet.</div>
                    )}
                </div>
            </div>
        </div>
    );

    // --- VIEW: INSIGHTS (Screen 4) ---
    const renderInsights = () => (
        <div className="fade-in">
            {/* Nav Header */}
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '40px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <button onClick={() => setView('overview')} className="icon-btn-refined" style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
                        <ArrowLeft size={24} color={COLORS.textMain} />
                    </button>
                    <div>
                        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '4px 12px', borderRadius: '20px', backgroundColor: `${COLORS.accentOchre}20`, color: COLORS.accentOchre, fontSize: '0.75rem', fontWeight: 'bold', marginBottom: '4px', textTransform: 'uppercase' }}>
                            <Lightbulb size={14} /> Kisan AI Assistant
                        </div>
                        <h2 style={{ fontSize: '2rem', fontWeight: '900', color: COLORS.textMain, margin: '0' }}>Profit Insights</h2>
                    </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', color: COLORS.textSec }}>
                    Updated: Today
                </div>
            </div>

            {/* Insight Cards Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '24px', marginBottom: '48px' }}>
                <div style={{ backgroundColor: 'white', borderRadius: '24px', padding: '32px', border: `1px solid ${COLORS.primary}50`, position: 'relative', overflow: 'hidden' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                        <div style={{ padding: '10px', backgroundColor: `${COLORS.primary}20`, borderRadius: '12px', color: COLORS.primaryDark }}>
                            <Droplets size={24} />
                        </div>
                        <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: COLORS.textMain, margin: 0 }}>Cost Savings</h3>
                    </div>
                    <p style={{ fontSize: '1.75rem', fontWeight: '900', color: COLORS.textMain, marginBottom: '8px' }}>
                        You saved <span style={{ color: COLORS.primaryDark }}>₹2,000</span> by using drip irrigation.
                    </p>
                    <div style={{ display: 'flex', gap: '12px', marginTop: '24px' }}>
                        <button className="btn-secondary-small" style={{ padding: '8px 16px', borderRadius: '8px', border: '1px solid #ccc', background: 'white', cursor: 'pointer' }}>Ask "Why?"</button>
                    </div>
                </div>

                <div style={{ backgroundColor: 'white', borderRadius: '24px', padding: '32px', border: `1px solid ${COLORS.accentAlert}50`, position: 'relative', overflow: 'hidden' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                        <div style={{ padding: '10px', backgroundColor: `${COLORS.accentAlert}20`, borderRadius: '12px', color: COLORS.accentAlert }}>
                            <AlertCircle size={24} />
                        </div>
                        <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: COLORS.textMain, margin: 0 }}>Expense Alert</h3>
                    </div>
                    <p style={{ fontSize: '1.75rem', fontWeight: '900', color: COLORS.textMain, marginBottom: '8px' }}>
                        Fertilizer cost is <span style={{ color: COLORS.accentAlert }}>15% higher</span> than last season.
                    </p>
                    <div style={{ display: 'flex', gap: '12px', marginTop: '24px' }}>
                        <button className="btn-secondary-small" style={{ padding: '8px 16px', borderRadius: '8px', border: '1px solid #ccc', background: 'white', cursor: 'pointer' }}>Ask "Why?"</button>
                    </div>
                </div>
            </div>

            {/* Smart Recommendations */}
            <div>
                <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: COLORS.textMain, marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <Lightbulb size={28} color={COLORS.accentOchre} fill={COLORS.accentOchre} /> Smart Recommendations
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '24px' }}>
                    {insights.suggestions.length > 0 ? insights.suggestions.map((sug, i) => (
                        <RecommendationCard key={i} category="Optimization" title={sug.suggestionTitle} desc={sug.whyThisHelps} />
                    )) : (
                        <>
                            <RecommendationCard category="Input Cost" title="Reduce input cost" desc="Switching to organic compost for 30% of your land can save ₹1,500/acre." />
                            <RecommendationCard category="Market Timing" title="Change selling time" desc="Wheat prices are predicted to rise by 8% in the next 15 days." />
                        </>
                    )}
                </div>
            </div>
        </div>
    );

    return (
        <div style={{ paddingBottom: '80px', maxWidth: '1200px', margin: '0 auto' }}>
            {view === 'overview' && renderOverview()}
            {view === 'crop-profit' && renderCropProfit()}
            {view === 'expenses' && renderExpenses()}
            {view === 'insights' && renderInsights()}

            <AddTransactionModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onSave={handleAddTransaction}
            />
        </div>
    );
};

// --- Helper Components ---

const SummaryCard = ({ title, amount, trend, trendColor, icon: Icon, iconColor, bgColor }) => (
    <div style={{ backgroundColor: 'white', borderRadius: '16px', padding: '24px', border: '1px solid #E6DCC8', boxShadow: '0 2px 4px rgba(0,0,0,0.02)' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
            <div style={{ padding: '8px', backgroundColor: bgColor || 'white', borderRadius: '8px' }}>
                <Icon size={24} color={iconColor} />
            </div>
            <span style={{ fontSize: '0.85rem', fontWeight: 'bold', textTransform: 'uppercase', color: iconColor }}>{title}</span>
        </div>
        <div style={{ fontSize: '2.5rem', fontWeight: '900', color: COLORS.textMain, lineHeight: 1 }}>{amount}</div>
        <div style={{ marginTop: '12px', display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.85rem', fontWeight: 'bold', color: trendColor, backgroundColor: '#F9FAFB', width: 'fit-content', padding: '4px 8px', borderRadius: '12px' }}>
            <TrendingUp size={14} /> {trend}
        </div>
    </div>
);

const NavBigButton = ({ title, desc, icon: Icon, iconColor, onClick }) => (
    <button onClick={onClick} className="hover-scale" style={{
        display: 'flex', alignItems: 'center', gap: '24px',
        padding: '24px', borderRadius: '24px', backgroundColor: COLORS.cardBeige,
        border: '1px solid #E6DCC8', width: '100%', textAlign: 'left', cursor: 'pointer'
    }}>
        <div style={{ width: '64px', height: '64px', borderRadius: '16px', backgroundColor: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
            <Icon size={32} color={iconColor} />
        </div>
        <div style={{ flex: 1 }}>
            <h4 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: COLORS.textMain, margin: '0 0 4px 0' }}>{title}</h4>
            <p style={{ margin: 0, color: COLORS.textSec }}>{desc}</p>
        </div>
        <ChevronRight size={24} color={COLORS.textSec} />
    </button>
);

const ExpenseCategory = ({ title, amount, color, icon: Icon }) => {
    const colorMap = {
        green: { bg: '#E8F5E9', text: '#2E7D32' },
        blue: { bg: '#E3F2FD', text: '#1565C0' },
        orange: { bg: '#FFF3E0', text: '#EF6C00' },
        red: { bg: '#FFEBEE', text: '#C62828' }
    };
    const theme = colorMap[color];
    return (
        <div className="hover-scale" style={{ backgroundColor: 'white', padding: '24px', borderRadius: '16px', border: '1px solid #E6DCC8', cursor: 'pointer' }}>
            <div style={{ width: '48px', height: '48px', borderRadius: '12px', backgroundColor: theme.bg, color: theme.text, display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '12px' }}>
                <Icon size={24} />
            </div>
            <h4 style={{ fontSize: '1.1rem', fontWeight: 'bold', color: COLORS.textMain, margin: '0 0 4px 0' }}>{title}</h4>
            <p style={{ margin: 0, color: COLORS.textSec, fontSize: '0.9rem' }}>{amount} spent</p>
        </div>
    );
};

const TransactionRow = ({ title, date, amount, iconColor, icon: Icon }) => {
    const colorMap = {
        green: { bg: '#E8F5E9', text: '#2E7D32' },
        blue: { bg: '#E3F2FD', text: '#1565C0' },
        orange: { bg: '#FFF3E0', text: '#EF6C00' },
        red: { bg: '#FFEBEE', text: '#C62828' }
    };
    const theme = colorMap[iconColor] || colorMap.blue;
    return (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '16px 24px', borderBottom: '1px solid #E6DCC8' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <div style={{ width: '40px', height: '40px', borderRadius: '50%', backgroundColor: theme.bg, color: theme.text, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Icon size={20} />
                </div>
                <div>
                    <div style={{ fontWeight: 'bold', color: COLORS.textMain }}>{title}</div>
                    <div style={{ fontSize: '0.8rem', color: COLORS.textSec }}>{date}</div>
                </div>
            </div>
            <div style={{ fontWeight: 'bold', color: COLORS.textMain }}>{amount}</div>
        </div>
    );
};

const RecommendationCard = ({ category, title, desc }) => (
    <div className="hover-scale" style={{ backgroundColor: '#F2EFE5', borderRadius: '16px', padding: '24px', border: '1px solid #E6DCC8', display: 'flex', flexDirection: 'column', height: '100%', cursor: 'pointer' }}>
        <div style={{ marginBottom: '16px' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 'bold', backgroundColor: 'white', padding: '4px 8px', borderRadius: '4px', border: '1px solid #E6DCC8', color: COLORS.textSec }}>{category}</span>
        </div>
        <h4 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: COLORS.textMain, marginBottom: '12px' }}>{title}</h4>
        <p style={{ fontSize: '0.9rem', color: COLORS.textSec, flex: 1, lineHeight: 1.6 }}>{desc}</p>
        <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid rgba(0,0,0,0.05)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: COLORS.primary, fontWeight: 'bold', fontSize: '0.9rem' }}>
            View Details <ChevronRight size={20} />
        </div>
    </div>
);

export default Finance;
