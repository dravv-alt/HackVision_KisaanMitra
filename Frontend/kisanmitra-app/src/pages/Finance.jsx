import React, { useState } from 'react';
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

const Finance = () => {
    // Navigation State: 'overview', 'crop-profit', 'expenses', 'insights'
    const [view, setView] = useState('overview');

    // --- Mock Data Source of Truth ---
    // Ensure logical consistency: Totals in dashboard = Sum of these crops
    const cropData = [
        { id: 1, name: 'Wheat', area: '15 Acres', income: 450000, expense: 180000, profit: 270000, status: 'Profitable', trend: 'up' },
        { id: 2, name: 'Mustard', area: '5 Acres', income: 120000, expense: 95000, profit: 25000, status: 'Low Margin', trend: 'down' },
        { id: 3, name: 'Chickpea (Chana)', area: '8 Acres', income: 280000, expense: 120000, profit: 160000, status: 'Profitable', trend: 'up' },
    ];

    // --- State: Transactions ---
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [transactions, setTransactions] = useState([
        { id: 1, title: "Wheat Seeds", date: "Today, 10:30 AM", amount: "- ₹500", type: "expense", category: "Seeds" },
        { id: 2, title: "Harvest Labor", date: "Yesterday, 05:15 PM", amount: "- ₹1,200", type: "expense", category: "Labor" },
        { id: 3, title: "Tractor Diesel", date: "Oct 24, 09:00 AM", amount: "- ₹1,650", type: "expense", category: "Machinery" },
        { id: 4, title: "Urea Bags (x5)", date: "Oct 22, 02:45 PM", amount: "- ₹2,100", type: "expense", category: "Fertilizers" },
    ]);

    const handleAddTransaction = (newTx) => {
        // Format amount string based on type
        const amountStr = newTx.type === 'expense'
            ? `- ₹${newTx.amount}`
            : `+ ₹${newTx.amount}`;

        const txToAdd = {
            id: newTx.id,
            title: newTx.title,
            date: "Just now", // Simplified for demo
            amount: amountStr,
            type: newTx.type,
            category: newTx.category
        };

        setTransactions([txToAdd, ...transactions]);
    };

    const totalIncome = cropData.reduce((acc, curr) => acc + curr.income, 0);
    const totalExpense = cropData.reduce((acc, curr) => acc + curr.expense, 0);
    const netProfit = totalIncome - totalExpense;

    // Formatting Helper
    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumSignificantDigits: 3
        }).format(amount);
    };

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
                        border: `1px solid ${COLORS.accentOchre}40`, fontWeight: 'bold'
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
                    amount={formatCurrency(totalIncome)}
                    trend="+12% from last season"
                    trendColor={COLORS.primaryDark} // Using dark green as trend up color
                    icon={Wallet}
                    iconColor={COLORS.primary}
                    bgColor="rgba(143, 168, 146, 0.1)"
                />
                <SummaryCard
                    title="Total Expenses"
                    amount={formatCurrency(totalExpense)}
                    trend="Mostly seeds & fertilizer"
                    trendColor={COLORS.textSec}
                    icon={ArrowDownRight}
                    iconColor={COLORS.accentAlert}
                    bgColor="rgba(217, 114, 76, 0.1)"
                />
                <SummaryCard
                    title="Net Profit"
                    amount={formatCurrency(netProfit)}
                    trend="Healthy margin"
                    trendColor={COLORS.primaryDark}
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
                    gridColumn: 'span 1' // Simplified layout
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
                        Inflow is <strong style={{ color: COLORS.primaryDark }}>3.7x higher</strong> than outflow.
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
                    <button onClick={() => setView('overview')} className="icon-btn-refined">
                        <ArrowLeft size={24} color={COLORS.textMain} />
                    </button>
                    <div>
                        <h2 style={{ fontSize: '2rem', fontWeight: '900', color: COLORS.textMain, margin: '0' }}>Crop-Wise Performance</h2>
                        <p style={{ color: COLORS.textSec }}>Financial Year 2023-24</p>
                    </div>
                </div>
                <button className="btn-secondary" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Download size={18} /> Export Report
                </button>
            </div>

            {/* List */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                {cropData.map((crop) => (
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
                    <button onClick={() => setView('overview')} className="icon-btn-refined">
                        <ArrowLeft size={24} color={COLORS.textMain} />
                    </button>
                    <div>
                        <h2 style={{ fontSize: '2rem', fontWeight: '900', color: COLORS.textMain, margin: '0' }}>Financial Tracking</h2>
                        <p style={{ color: COLORS.textSec }}>Track every rupee spent (Oct View)</p>
                    </div>
                </div>
                <div style={{ padding: '8px 16px', backgroundColor: COLORS.cardBeige, borderRadius: '12px', border: `1px solid ${COLORS.accentAlert}40` }}>
                    <span style={{ fontSize: '0.85rem', fontWeight: 'bold', color: COLORS.textSec, textTransform: 'uppercase' }}>Total Oct Expenses</span>
                    <div style={{ fontSize: '1.5rem', fontWeight: '900', color: COLORS.textMain }}>₹14,250</div>
                </div>
            </div>

            {/* Categories */}
            <div style={{ marginBottom: '40px' }}>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: COLORS.textMain, marginBottom: '16px' }}>Categories</h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '16px' }}>
                    <ExpenseCategory title="Seeds" amount="₹3,200" color="green" icon={Leaf} />
                    <ExpenseCategory title="Fertilizers" amount="₹5,400" color="blue" icon={Droplets} />
                    <ExpenseCategory title="Labor" amount="₹4,000" color="orange" icon={Users} />
                    <ExpenseCategory title="Machinery" amount="₹1,650" color="red" icon={Tractor} />
                </div>
            </div>

            {/* Transactions List */}
            <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: COLORS.textMain }}>Recent Transactions</h3>
                    <button style={{ color: COLORS.primary, fontWeight: 'bold' }}>View All</button>
                </div>
                <div style={{ backgroundColor: 'white', borderRadius: '16px', border: '1px solid #E6DCC8', overflow: 'hidden' }}>
                    {transactions.map((tx) => (
                        <TransactionRow
                            key={tx.id}
                            title={tx.title}
                            date={tx.date}
                            amount={tx.amount}
                            iconColor={
                                tx.category === 'Seeds' ? 'green' :
                                    tx.category === 'Labor' ? 'orange' :
                                        tx.category === 'Machinery' ? 'red' : 'blue'
                            }
                            icon={
                                tx.category === 'Seeds' ? Leaf :
                                    tx.category === 'Labor' ? Users :
                                        tx.category === 'Machinery' ? Tractor : Droplets
                            }
                        />
                    ))}
                </div>
            </div>

            {/* Floating Voice Action (Static Visual) */}
            <div style={{ position: 'fixed', bottom: '30px', right: '30px', display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '16px', pointerEvents: 'none' }}>
                <div style={{ backgroundColor: 'rgba(255,255,255,0.95)', padding: '12px 20px', borderRadius: '16px', boxShadow: '0 8px 32px rgba(0,0,0,0.1)', border: '1px solid #E6DCC8', maxWidth: '300px' }}>
                    <p style={{ margin: 0, fontWeight: '500' }}><span style={{ color: COLORS.primary, fontWeight: 'bold' }}>🎙️ Say:</span> "Add ₹500 for seeds for Wheat"</p>
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
                    <button onClick={() => setView('overview')} className="icon-btn-refined">
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
                    Updated: Today, 10:30 AM
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
                        <button className="btn-secondary-small">Ask "Why?"</button>
                        <button style={{ background: 'none', border: 'none', color: COLORS.primaryDark, fontWeight: 'bold', cursor: 'pointer' }}>View Report →</button>
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
                        <button className="btn-secondary-small">Ask "Why?"</button>
                        <button style={{ background: 'none', border: 'none', color: COLORS.accentAlert, fontWeight: 'bold', cursor: 'pointer' }}>Compare Prices →</button>
                    </div>
                </div>
            </div>

            {/* Smart Recommendations */}
            <div>
                <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: COLORS.textMain, marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <Lightbulb size={28} color={COLORS.accentOchre} fill={COLORS.accentOchre} /> Smart Recommendations
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '24px' }}>
                    <RecommendationCard category="Input Cost" title="Reduce input cost" desc="Switching to organic compost for 30% of your land can save ₹1,500/acre." />
                    <RecommendationCard category="Market Timing" title="Change selling time" desc="Wheat prices are predicted to rise by 8% in the next 15 days." />
                    <RecommendationCard category="Subsidy" title="Apply for Solar Pump" desc="New scheme opened for solar pumps in your district. Reduces electricity bill." />
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
    const theme = colorMap[iconColor];
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
