import React, { useState } from 'react';
import {
    Menu, User, BarChart, Plus, ArrowRight, Sprout,
    Leaf, Droplets, Tractor, AlertTriangle, ArrowLeft,
    Clock, RefreshCw, AlertCircle, TrendingUp, MoreVertical,
    Home, CheckCircle, Search, Package
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import '../styles/global.css';

// --- Colors from Reference ---
const COLORS = {
    primary: "#8FA892", // Sage Green
    primaryDark: "#758E78",
    accentOchre: "#D9A54C", // Mustard
    accentAlert: "#D9724C", // Terracotta
    bgLight: "#FDFCF6", // Warm Beige
    cardBeige: "#F2EFE5",
    textMain: "#423E37", // Dark Grey/Brown
    textSec: "#6B6358"
};

const Inventory = () => {
    const navigate = useNavigate();
    const [view, setView] = useState('dashboard'); // 'dashboard', 'fertilizers', 'harvest', 'add'

    // --- Render Functions ---

    const renderDashboard = () => (
        <div className="fade-in">
            {/* Header / Title Section */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', marginBottom: '40px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '16px' }}>
                    <div>
                        <h2 style={{ fontSize: '2.5rem', fontWeight: '900', color: COLORS.textMain, margin: 0, lineHeight: 1.2 }}>Inventory</h2>
                        <p style={{ fontSize: '1.1rem', color: COLORS.textSec, marginTop: '8px' }}>Manage seeds, fertilizers, crops, and farm equipment.</p>
                    </div>
                    <div style={{ display: 'flex', gap: '12px' }}>
                        <button style={{
                            display: 'flex', alignItems: 'center', gap: '8px',
                            padding: '12px 24px', borderRadius: '12px',
                            backgroundColor: COLORS.cardBeige, color: COLORS.textMain,
                            border: `1px solid #E6DCC8`, fontWeight: 'bold',
                            cursor: 'pointer'
                        }}>
                            <BarChart size={20} /> View History
                        </button>
                        <button onClick={() => setView('add')} style={{
                            display: 'flex', alignItems: 'center', gap: '8px',
                            padding: '12px 24px', borderRadius: '12px',
                            backgroundColor: COLORS.primary, color: 'white',
                            border: 'none', fontWeight: 'bold', boxShadow: '0 4px 14px rgba(143, 168, 146, 0.4)',
                            cursor: 'pointer'
                        }}>
                            <Plus size={20} /> Add Item
                        </button>
                    </div>
                </div>

                {/* Categories Scroll */}
                <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
                        <h3 style={{ fontSize: '1rem', fontWeight: 'bold', color: COLORS.textSec, textTransform: 'uppercase', letterSpacing: '1px' }}>Categories</h3>
                        <span style={{ fontSize: '0.9rem', color: COLORS.textSec, display: 'flex', alignItems: 'center', gap: '4px' }}>Scroll <ArrowRight size={14} /></span>
                    </div>
                    <div style={{ display: 'flex', gap: '24px', overflowX: 'auto', paddingBottom: '16px' }} className="hide-scrollbar">

                        {/* Seeds */}
                        <CategoryCard
                            title="Seeds"
                            count="12"
                            unit="varieties"
                            icon={Sprout}
                            color="#E8F5E9"
                            iconColor="#2E7D32"
                            status="In Stock"
                            statusColor="green"
                            onClick={() => console.log('Seeds clicked')}
                        />

                        {/* Fertilizers */}
                        <CategoryCard
                            title="Fertilizers"
                            count="4"
                            unit="types"
                            icon={Leaf}
                            color="#FFF3E0"
                            iconColor="#EF6C00"
                            status="Low Stock"
                            statusColor="red"
                            isAlert={true}
                            onClick={() => setView('fertilizers')}
                        />

                        {/* Pesticides */}
                        <CategoryCard
                            title="Pesticides"
                            count="6"
                            unit="bottles"
                            icon={Droplets}
                            color="#E3F2FD"
                            iconColor="#1565C0"
                            status="Sufficient"
                            statusColor="blue"
                            onClick={() => console.log('Pesticides clicked')}
                        />

                        {/* Harvested Crops */}
                        <CategoryCard
                            title="Harvested Crops"
                            count="250"
                            unit="Quintals"
                            icon={Sprout}
                            color="#FFF8E1"
                            iconColor="#F57F17"
                            status="Stored"
                            statusColor="yellow"
                            onClick={() => setView('harvest')}
                        />

                        {/* Equipment */}
                        <CategoryCard
                            title="Equipment"
                            count="3"
                            unit="machines"
                            icon={Tractor}
                            color="#F5F5F5"
                            iconColor="#616161"
                            status="Operational"
                            statusColor="gray"
                            onClick={() => console.log('Equipment clicked')}
                        />
                    </div>
                </div>

                {/* Critical Alerts */}
                <div>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: COLORS.textMain, marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <AlertTriangle color={COLORS.accentAlert} /> Critical Alerts
                    </h3>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '24px' }}>

                        {/* Alert 1 */}
                        <div style={{ backgroundColor: '#FFEBEE', borderRadius: '16px', padding: '24px', border: '1px solid #FFCDD2', position: 'relative', overflow: 'hidden' }}>
                            <AlertCircle size={100} color="#D32F2F" style={{ position: 'absolute', right: '-20px', top: '-20px', opacity: 0.1 }} />
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                                <div style={{ padding: '8px', backgroundColor: 'white', borderRadius: '8px' }}>
                                    <AlertTriangle size={20} color="#D32F2F" />
                                </div>
                                <span style={{ color: '#C62828', fontWeight: 'bold', fontSize: '0.8rem', textTransform: 'uppercase' }}>Stock Alert</span>
                            </div>
                            <h4 style={{ fontSize: '1.5rem', fontWeight: '900', color: COLORS.textMain, marginBottom: '8px' }}>Low Urea Stock</h4>
                            <p style={{ fontSize: '1rem', color: COLORS.textMain, marginBottom: '24px', lineHeight: 1.5 }}>
                                Your current stock is <strong style={{ color: '#D32F2F' }}>2 bags</strong>. Upcoming sowing cycle requires approx <strong>10 bags</strong>.
                            </p>
                            <button style={{ backgroundColor: '#D32F2F', color: 'white', padding: '12px 24px', borderRadius: '12px', border: 'none', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                                Order Now <ArrowRight size={18} />
                            </button>
                        </div>

                        {/* Alert 2 */}
                        <div style={{ backgroundColor: '#FFF8E1', borderRadius: '16px', padding: '24px', border: '1px solid #FFECB3', position: 'relative', overflow: 'hidden' }}>
                            <Droplets size={100} color="#F57F17" style={{ position: 'absolute', right: '-20px', top: '-20px', opacity: 0.1 }} />
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                                <div style={{ padding: '8px', backgroundColor: 'white', borderRadius: '8px' }}>
                                    <TrendingUp size={20} color="#F57F17" />
                                </div>
                                <span style={{ color: '#EF6C00', fontWeight: 'bold', fontSize: '0.8rem', textTransform: 'uppercase' }}>Quality Risk</span>
                            </div>
                            <h4 style={{ fontSize: '1.5rem', fontWeight: '900', color: COLORS.textMain, marginBottom: '8px' }}>Stored Wheat Spoilage</h4>
                            <p style={{ fontSize: '1rem', color: COLORS.textMain, marginBottom: '24px', lineHeight: 1.5 }}>
                                High moisture levels detected in <strong style={{ color: '#E65100' }}>Silo #2</strong>. Inspection recommended.
                            </p>
                            <button style={{ backgroundColor: 'white', color: '#EF6C00', padding: '12px 24px', borderRadius: '12px', border: '2px solid #FFE082', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                                View Details <ArrowRight size={18} />
                            </button>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    );

    const renderFertilizers = () => (
        <div className="fade-in">
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '32px' }}>
                <button onClick={() => setView('dashboard')} style={{ width: '40px', height: '40px', borderRadius: '50%', border: `1px solid ${COLORS.accentOchre}`, backgroundColor: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }}>
                    <ArrowLeft size={20} color={COLORS.textSec} />
                </button>
                <div>
                    <h2 style={{ fontSize: '2rem', fontWeight: '900', color: COLORS.textMain, margin: 0 }}>Fertilizers</h2>
                    <p style={{ color: COLORS.textSec }}>Inventory Management & Usage Tracking</p>
                </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                <FertilizerItem
                    name="Urea"
                    qty="150"
                    unit="kg"
                    status="Low Stock"
                    lastUsed="3 days ago"
                    icon={Leaf}
                    colorTheme="amber"
                />
                <FertilizerItem
                    name="DAP"
                    qty="450"
                    unit="kg"
                    status="Healthy"
                    lastUsed="1 week ago"
                    icon={Beaker} // Using placeholder visual for generic 'Chemical'
                    colorTheme="green"
                />
                <FertilizerItem
                    name="MOP (Potash)"
                    qty="220"
                    unit="kg"
                    status="Healthy"
                    lastUsed="2 weeks ago"
                    icon={Leaf}
                    colorTheme="standard"
                />
            </div>
        </div>
    );

    const renderHarvest = () => (
        <div className="fade-in">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <button onClick={() => setView('dashboard')} style={{ width: '40px', height: '40px', borderRadius: '50%', border: `1px solid ${COLORS.accentOchre}`, backgroundColor: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }}>
                        <ArrowLeft size={20} color={COLORS.textSec} />
                    </button>
                    <div>
                        <h2 style={{ fontSize: '2rem', fontWeight: '900', color: COLORS.textMain, margin: 0 }}>Harvest Storage</h2>
                        <p style={{ color: COLORS.textSec }}>Track stored crops & spoilage risks</p>
                    </div>
                </div>
                <button style={{ backgroundColor: COLORS.primary, color: 'white', padding: '10px 20px', borderRadius: '8px', border: 'none', fontWeight: 'bold', display: 'flex', gap: '8px', cursor: 'pointer' }}>
                    <Plus size={18} /> Add Harvest
                </button>
            </div>

            {/* AI Insight Card */}
            <div style={{
                background: `linear-gradient(to right, #F0F7F4, #E8F3EB)`,
                borderRadius: '16px', padding: '32px', border: `1px solid rgba(143, 168, 146, 0.3)`,
                marginBottom: '40px', position: 'relative', overflow: 'hidden'
            }}>
                <div style={{ display: 'flex', gap: '24px', position: 'relative', zIndex: 1 }}>
                    <div style={{ width: '48px', height: '48px', backgroundColor: COLORS.primary, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                        <TrendingUp size={24} color="white" />
                    </div>
                    <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                            <span style={{ fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase', color: COLORS.primaryDark }}>AI Insight</span>
                            <span style={{ fontSize: '0.75rem', color: COLORS.textSec }}>• Based on market trends</span>
                        </div>
                        <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '8px', color: COLORS.textMain }}>Sell 40% of Wheat stock now</h3>
                        <p style={{ fontSize: '1.1rem', color: COLORS.textSec, lineHeight: 1.6, marginBottom: '24px', maxWidth: '800px' }}>
                            Moisture levels in Warehouse A are rising. Additionally, wheat prices are currently peaking at ₹2,450/quintal. Selling now maximizes profit.
                        </p>
                        <div style={{ display: 'flex', gap: '12px' }}>
                            <button style={{ backgroundColor: 'white', border: `1px solid ${COLORS.primary}`, padding: '10px 20px', borderRadius: '20px', color: COLORS.textMain, fontWeight: '600', cursor: 'pointer' }}>Market Guide</button>
                            <button style={{ backgroundColor: 'rgba(143, 168, 146, 0.2)', border: 'none', padding: '10px 20px', borderRadius: '20px', color: COLORS.primaryDark, fontWeight: '600', cursor: 'pointer' }}>Not now</button>
                        </div>
                    </div>
                </div>
            </div>

            <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '8px', color: COLORS.textMain }}>
                <Package size={24} /> Current Inventory
            </h3>

            {/* Harvest Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
                <HarvestItem
                    crop="Wheat"
                    harvestDate="Apr 15"
                    qty="50"
                    location="Warehouse A"
                    risk="Medium"
                    riskLevel={45}
                    riskColor={COLORS.accentOchre}
                    statusText="Check moisture"
                />
                <HarvestItem
                    crop="Mustard"
                    harvestDate="Mar 20"
                    qty="120"
                    location="Home Silo"
                    risk="Low"
                    riskLevel={15}
                    riskColor={COLORS.primary}
                    statusText="Safe condition"
                />
                <HarvestItem
                    crop="Soybean"
                    harvestDate="Oct 10"
                    qty="10"
                    location="Warehouse B"
                    risk="High"
                    riskLevel={85}
                    riskColor={COLORS.accentAlert}
                    statusText="Pests detected!"
                />
            </div>
        </div>
    );

    // Reusing user's wizard concept but just simpler placeholder as per the HTML flow focus
    const renderAddWizard = () => (
        <div style={{ textAlign: 'center', padding: '40px' }}>
            <h2 style={{ fontSize: '2rem' }}>Add Item Wizard</h2>
            <p style={{ marginBottom: '20px' }}>Wizard steps 1-3 would go here...</p>
            <button onClick={() => setView('dashboard')} style={{ padding: '10px 20px', borderRadius: '8px', backgroundColor: COLORS.primary, color: 'white', border: 'none', cursor: 'pointer' }}>Back to Dashboard</button>
        </div>
    );

    return (
        <div style={{ paddingBottom: '80px', maxWidth: '1200px', margin: '0 auto' }}>
            {view === 'dashboard' && renderDashboard()}
            {view === 'fertilizers' && renderFertilizers()}
            {view === 'harvest' && renderHarvest()}
            {view === 'add' && renderAddWizard()}
        </div>
    );
};

// --- Helper Components ---

const CategoryCard = ({ title, count, unit, icon: Icon, color, iconColor, status, statusColor, isAlert, onClick }) => (
    <div onClick={onClick} className="hover-scale" style={{
        minWidth: '260px',
        backgroundColor: 'white',
        borderRadius: '16px',
        padding: '24px',
        border: isAlert ? `2px solid ${COLORS.accentAlert}` : '1px solid #E6DCC8',
        cursor: 'pointer',
        boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
        transition: 'transform 0.2s',
        scrollSnapAlign: 'start'
    }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
            <div style={{ padding: '12px', borderRadius: '12px', backgroundColor: color }}>
                <Icon size={32} color={iconColor} />
            </div>
            <span style={{
                fontSize: '0.75rem', fontWeight: 'bold',
                backgroundColor: statusColor === 'red' ? '#FFEBEE' : statusColor === 'green' ? '#E8F5E9' : statusColor === 'yellow' ? '#FFF8E1' : '#F5F5F5',
                color: statusColor === 'red' ? '#C62828' : statusColor === 'green' ? '#2E7D32' : statusColor === 'yellow' ? '#F57F17' : '#616161',
                padding: '4px 8px', borderRadius: '12px'
            }}>
                {status}
            </span>
        </div>
        <h4 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: COLORS.textMain, margin: '0 0 4px 0' }}>{title}</h4>
        <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
            <span style={{ fontSize: '2rem', fontWeight: '900', color: COLORS.textMain }}>{count}</span>
            <span style={{ color: COLORS.textSec, fontWeight: '500' }}>{unit}</span>
        </div>
    </div>
);

const FertilizerItem = ({ name, qty, unit, status, lastUsed, icon: Icon, colorTheme }) => {
    let badgeBg = '#E8F5E9', badgeText = '#2E7D32', badgeIcon = CheckCircle;
    if (colorTheme === 'amber') { badgeBg = '#FFF8E1'; badgeText = '#EF6C00'; badgeIcon = AlertTriangle; }

    return (
        <div style={{ backgroundColor: 'white', borderRadius: '16px', padding: '24px', border: '1px solid #E6DCC8', display: 'flex', flexWrap: 'wrap', gap: '24px', alignItems: 'center', boxShadow: '0 2px 4px rgba(0,0,0,0.02)' }}>
            <div style={{ width: '64px', height: '64px', borderRadius: '16px', backgroundColor: COLORS.cardBeige, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Icon size={32} color={COLORS.textSec} />
            </div>
            <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                    <h3 style={{ fontSize: '1.5rem', fontWeight: '900', margin: 0, color: COLORS.textMain }}>{name}</h3>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.75rem', fontWeight: 'bold', padding: '4px 8px', borderRadius: '12px', backgroundColor: badgeBg, color: badgeText, textTransform: 'uppercase' }}>
                        {status}
                    </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <span style={{ fontSize: '1.5rem', fontWeight: '900', color: COLORS.textMain }}>{qty} <span style={{ fontSize: '1rem', color: COLORS.textSec, fontWeight: 'normal' }}>{unit}</span></span>
                    <span style={{ fontSize: '0.85rem', color: COLORS.textSec, display: 'flex', alignItems: 'center', gap: '4px', backgroundColor: COLORS.bgLight, padding: '4px 8px', borderRadius: '4px', border: '1px solid #E6DCC8' }}>
                        <Clock size={14} /> Last Used: {lastUsed}
                    </span>
                </div>
            </div>
            <div style={{ display: 'flex', gap: '12px' }}>
                <button style={{ padding: '10px 24px', borderRadius: '8px', backgroundColor: 'rgba(143, 168, 146, 0.1)', color: COLORS.primaryDark, fontWeight: 'bold', border: 'none', cursor: 'pointer' }}>Used</button>
                <button style={{ padding: '10px 24px', borderRadius: '8px', backgroundColor: COLORS.primary, color: 'white', fontWeight: 'bold', border: 'none', cursor: 'pointer' }}>Add</button>
            </div>
        </div>
    );
};

const HarvestItem = ({ crop, harvestDate, qty, location, risk, riskLevel, riskColor, statusText }) => (
    <div className="hover-scale" style={{ backgroundColor: 'white', borderRadius: '16px', padding: '24px', border: '1px solid #E6DCC8', position: 'relative', overflow: 'hidden', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', transition: 'transform 0.2s', cursor: 'pointer' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
            <div style={{ display: 'flex', gap: '12px' }}>
                <div style={{ width: '48px', height: '48px', borderRadius: '12px', backgroundColor: COLORS.bgLight, border: '1px solid #E6DCC8', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Sprout size={24} color={COLORS.accentOchre} />
                </div>
                <div>
                    <h4 style={{ fontSize: '1.1rem', fontWeight: 'bold', margin: 0, color: COLORS.textMain }}>{crop}</h4>
                    <span style={{ fontSize: '0.75rem', color: COLORS.textSec, backgroundColor: COLORS.bgLight, padding: '2px 6px', borderRadius: '4px' }}>Harvested: {harvestDate}</span>
                </div>
            </div>
            <MoreVertical size={20} color={COLORS.textSec} />
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', borderBottom: '1px dashed #E6DCC8', paddingBottom: '12px', marginBottom: '12px' }}>
            <div>
                <div style={{ fontSize: '0.75rem', fontWeight: 'bold', color: COLORS.textSec, textTransform: 'uppercase' }}>Quantity</div>
                <div style={{ fontSize: '1.5rem', fontWeight: '900', color: COLORS.textMain }}>{qty} <span style={{ fontSize: '0.9rem', color: COLORS.textSec, fontWeight: 'medium' }}>Quintals</span></div>
            </div>
            <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 'bold', color: COLORS.textSec, textTransform: 'uppercase' }}>Location</div>
                <div style={{ fontSize: '0.9rem', fontWeight: '500', color: COLORS.textMain, display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Home size={14} /> {location}
                </div>
            </div>
        </div>

        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                <span style={{ fontSize: '0.75rem', fontWeight: 'bold', color: COLORS.textSec }}>Spoilage Risk</span>
                <span style={{ fontSize: '0.75rem', fontWeight: 'bold', color: riskColor }}>{risk} Risk</span>
            </div>
            <div style={{ width: '100%', height: '10px', backgroundColor: '#F5F5F5', borderRadius: '5px', overflow: 'hidden', marginBottom: '6px' }}>
                <div style={{ width: `${riskLevel}%`, height: '100%', backgroundColor: riskColor }}></div>
            </div>
            <p style={{ fontSize: '0.7rem', color: COLORS.textSec }}>{statusText}</p>
        </div>

        <div style={{ marginTop: '20px', paddingTop: '16px', borderTop: '1px solid #E6DCC8', display: 'flex', gap: '12px' }}>
            <button style={{ flex: 1, padding: '8px', fontSize: '0.85rem', fontWeight: 'bold', color: COLORS.primaryDark, backgroundColor: 'rgba(143, 168, 146, 0.1)', border: 'none', borderRadius: '8px' }}>Details</button>
            <button style={{ flex: 1, padding: '8px', fontSize: '0.85rem', fontWeight: 'bold', color: COLORS.textMain, backgroundColor: COLORS.cardBeige, border: 'none', borderRadius: '8px' }}>Sell</button>
        </div>
    </div>
);

const Beaker = ({ size, color }) => <div style={{ width: size, height: size, fontSize: size, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>🧪</div>;

export default Inventory;
