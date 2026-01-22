import React from 'react';
import {
    ShieldCheck, Landmark, Handshake, Sprout, Sparkles,
    IndianRupee, Info, Eye, Umbrella, CheckCircle,
    ArrowRight, CreditCard, FileSignature, Mountain, Ban,
    Search, Filter
} from 'lucide-react';
import '../styles/global.css';

const GovernmentSchemes = () => {
    // --- Colors matching the design ---
    const colors = {
        primary: '#8FA892',
        primaryDark: '#758E78',
        accentOchre: '#D9A54C',
        backgroundLight: '#FDFCF6',
        cardBeige: '#F2EFE5',
        textMain: '#423E37',
        textSecondary: '#6B6358',
    };

    const filters = [
        "All Schemes", "🌱 Crop Based", "📍 Location Based", "💰 Subsidy", "🛡️ Insurance", "🚜 Equipment"
    ];

    return (
        <div className="fade-in" style={{ paddingBottom: '80px', maxWidth: '1200px', margin: '0 auto' }}>

            {/* Header Hero Section */}
            <div style={{
                position: 'relative',
                backgroundColor: colors.cardBeige,
                borderRadius: '24px',
                padding: '40px',
                marginBottom: '40px',
                overflow: 'hidden',
                border: '1px solid #E6DCC8'
            }}>
                <div style={{ position: 'relative', zIndex: 10, maxWidth: '600px' }}>
                    <div style={{
                        display: 'inline-flex', alignItems: 'center', gap: '8px',
                        padding: '4px 12px', borderRadius: '20px',
                        backgroundColor: 'rgba(143, 168, 146, 0.1)',
                        color: colors.primaryDark,
                        marginBottom: '16px',
                        border: '1px solid rgba(143, 168, 146, 0.2)',
                        fontSize: '0.8rem', fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: '0.5px'
                    }}>
                        <ShieldCheck size={16} /> Government Verified
                    </div>
                    <h2 style={{
                        fontSize: '3rem', fontWeight: '900',
                        color: colors.textMain, marginBottom: '16px', lineHeight: 1.1
                    }}>
                        Find schemes made for <span style={{ color: colors.primaryDark }}>your farm</span>
                    </h2>
                    <p style={{ fontSize: '1.1rem', color: colors.textSecondary, marginBottom: '32px', lineHeight: 1.6 }}>
                        Unlock financial support, subsidies, and insurance plans tailored to your land size, crops, and location.
                    </p>
                    <button style={{
                        display: 'flex', alignItems: 'center', gap: '8px',
                        padding: '14px 28px', backgroundColor: colors.primary,
                        color: 'white', borderRadius: '12px',
                        fontSize: '1rem', fontWeight: 'bold', border: 'none',
                        boxShadow: '0 4px 14px rgba(143, 168, 146, 0.3)',
                        cursor: 'pointer'
                    }}>
                        Check Eligibility <ArrowRight size={20} />
                    </button>
                </div>

                {/* Decorative Background Icons (Abstracted) */}
                <div style={{ position: 'absolute', right: '-40px', bottom: '-40px', opacity: 0.1, pointerEvents: 'none' }}>
                    <Landmark size={300} color={colors.primaryDark} />
                </div>
            </div>

            {/* Filter Scroll */}
            <div style={{ marginBottom: '40px', overflowX: 'auto', paddingBottom: '8px' }} className="hide-scrollbar">
                <div style={{ display: 'flex', gap: '12px' }}>
                    {filters.map((filter, index) => (
                        <button key={index} style={{
                            whiteSpace: 'nowrap',
                            padding: '10px 20px',
                            borderRadius: '24px',
                            backgroundColor: index === 0 ? colors.textMain : 'white',
                            color: index === 0 ? 'white' : colors.textSecondary,
                            border: index === 0 ? 'none' : '1px solid #E6DCC8',
                            fontWeight: 'bold', fontSize: '0.9rem',
                            cursor: 'pointer',
                            display: 'flex', alignItems: 'center', gap: '6px'
                        }}>
                            {filter}
                        </button>
                    ))}
                </div>
            </div>

            {/* Recommended Section */}
            <div style={{ marginBottom: '48px' }}>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: colors.textMain, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Sparkles size={24} color={colors.accentOchre} fill={colors.accentOchre} /> Recommended for You
                </h3>

                <div style={{
                    backgroundColor: 'white', borderRadius: '24px', padding: '32px',
                    border: `2px solid rgba(217, 165, 76, 0.2)`,
                    position: 'relative', overflow: 'hidden',
                    boxShadow: '0 8px 30px rgba(217, 165, 76, 0.05)'
                }}>
                    <div style={{ display: 'flex', flexDirection: 'row', gap: '24px', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between' }}>
                        <div style={{ display: 'flex', gap: '20px', flex: 1, minWidth: '300px' }}>
                            <div style={{
                                width: '64px', height: '64px', borderRadius: '16px',
                                backgroundColor: 'rgba(217, 165, 76, 0.1)',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                color: colors.accentOchre, flexShrink: 0
                            }}>
                                <IndianRupee size={32} />
                            </div>
                            <div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                                    <h4 style={{ fontSize: '1.5rem', fontWeight: '900', color: colors.textMain, margin: 0 }}>PM-Kisan Samman Nidhi</h4>
                                    <span style={{ fontSize: '0.75rem', fontWeight: 'bold', backgroundColor: colors.accentOchre, color: 'white', padding: '2px 8px', borderRadius: '4px' }}>High Match</span>
                                </div>
                                <p style={{ fontSize: '1.1rem', color: colors.textSecondary, marginBottom: '12px' }}>
                                    Get <strong style={{ color: colors.textMain }}>₹6,000 per year</strong> as minimum income support.
                                </p>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', color: colors.textSecondary, backgroundColor: colors.cardBeige, padding: '6px 12px', borderRadius: '8px', width: 'fit-content' }}>
                                    <Info size={16} /> <span>Why? You own <strong>5 acres</strong> of land.</span>
                                </div>
                            </div>
                        </div>
                        <button style={{
                            whiteSpace: 'nowrap',
                            padding: '14px 28px', backgroundColor: colors.accentOchre,
                            color: 'white', borderRadius: '12px',
                            fontSize: '1rem', fontWeight: 'bold', border: 'none',
                            display: 'flex', alignItems: 'center', gap: '8px',
                            cursor: 'pointer', boxShadow: '0 4px 12px rgba(217, 165, 76, 0.2)'
                        }}>
                            View Details <Eye size={20} />
                        </button>
                    </div>
                </div>
            </div>

            {/* Available Grid */}
            <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: colors.textMain }}>Available Schemes</h3>
                    <span style={{ fontSize: '0.9rem', color: colors.textSecondary, fontWeight: '500' }}>Showing 4 results</span>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>

                    {/* PMFBY Card */}
                    <SchemeCard
                        title="Pradhan Mantri Fasal Bima Yojana"
                        desc="Comprehensive crop insurance coverage against non-preventable natural risks from pre-sowing to post-harvest."
                        icon={Umbrella}
                        iconColor="#2E7D32"
                        iconBg="#E8F5E9"
                        tag="Eligible"
                        tagIcon={CheckCircle}
                        tagColor="green"
                        footerLabel="Insurance"
                        footerAction="Apply Now"
                        borderHoverColor={colors.primary}
                    />

                    {/* KCC Card */}
                    <SchemeCard
                        title="Kisan Credit Card (KCC)"
                        desc="Get timely credit for cultivation needs, post-harvest expenses, and produce marketing loans."
                        icon={CreditCard}
                        iconColor="#1565C0"
                        iconBg="#E3F2FD"
                        tag="Apply Now"
                        tagIcon={FileSignature}
                        tagColor="gray"
                        footerLabel="Loan"
                        footerAction="View Details"
                        borderHoverColor={colors.primary}
                    />

                    {/* Soil Health Card */}
                    <SchemeCard
                        title="Soil Health Card Scheme"
                        desc="Assess nutrient status of your holding and get recommendations on dosage of nutrients."
                        icon={Mountain}
                        iconColor="#E65100"
                        iconBg="#FFF3E0"
                        tag="Eligible"
                        tagIcon={CheckCircle}
                        tagColor="green"
                        footerLabel="Advisory"
                        footerAction="Apply Now"
                        borderHoverColor={colors.primary}
                    />

                    {/* Agri-Mechanization (Closed) */}
                    <SchemeCard
                        title="Agri-Mechanization Subsidy"
                        desc="Financial assistance for purchasing farm equipment like tractors and power tillers."
                        icon={Tractor}
                        iconColor="#616161"
                        iconBg="#F5F5F5"
                        tag="Closed"
                        tagIcon={Ban}
                        tagColor="red"
                        footerLabel="Subsidy"
                        footerAction="Check Later"
                        isClosed={true}
                        borderHoverColor={colors.primary}
                    />
                </div>
            </div>
        </div>
    );
};

const SchemeCard = ({ title, desc, icon: Icon, iconColor, iconBg, tag, tagIcon: TagIcon, tagColor, footerLabel, footerAction, isClosed, borderHoverColor }) => {

    // Tag styles
    const tagStyles = {
        green: { bg: '#E8F5E9', text: '#2E7D32', border: '#C8E6C9' },
        gray: { bg: '#F5F5F5', text: '#616161', border: '#E0E0E0' },
        red: { bg: '#FFEBEE', text: '#C62828', border: '#FFCDD2' }
    };
    const currentTag = tagStyles[tagColor] || tagStyles.green;

    return (
        <div className="hover-scale" style={{
            backgroundColor: 'white', borderRadius: '16px', padding: '24px',
            border: '1px solid #E6DCC8', display: 'flex', flexDirection: 'column',
            cursor: 'pointer', transition: 'all 0.2s', opacity: isClosed ? 0.8 : 1
        }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                <div style={{
                    padding: '12px', borderRadius: '12px', backgroundColor: iconBg,
                    color: iconColor, display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>
                    <Icon size={28} />
                </div>
                <div style={{
                    display: 'flex', alignItems: 'center', gap: '4px',
                    padding: '4px 10px', borderRadius: '20px',
                    backgroundColor: currentTag.bg, color: currentTag.text,
                    border: `1px solid ${currentTag.border}`, fontSize: '0.75rem', fontWeight: 'bold'
                }}>
                    <TagIcon size={14} /> {tag}
                </div>
            </div>

            <div style={{ marginBottom: '16px' }}>
                <h4 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#423E37', marginBottom: '8px', lineHeight: 1.3 }}>{title}</h4>
                <p style={{ fontSize: '0.9rem', color: '#6B6358', lineHeight: 1.5, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    {desc}
                </p>
            </div>

            <div style={{
                marginTop: 'auto', paddingTop: '16px', borderTop: '1px solid #E6DCC8',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center'
            }}>
                <span style={{ fontSize: '0.75rem', fontWeight: 'bold', color: '#6B6358', textTransform: 'uppercase', letterSpacing: '0.5px' }}>{footerLabel}</span>
                <span style={{
                    fontSize: '0.9rem', fontWeight: 'bold', color: isClosed ? '#6B6358' : '#8FA892',
                    display: 'flex', alignItems: 'center', gap: '4px'
                }}>
                    {footerAction} {!isClosed && <ArrowRight size={16} />}
                </span>
            </div>
        </div>
    );
};

// Reusing Tractor icon since it wasn't in the import list above (though I put it there but 'Tractor' might not be in the initial import list for the main component, let me check)
// Ah, I missed importing Tractor in the main component. Adding it now.
const Tractor = ({ size, color }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color || "currentColor"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M3 4h9l1 7h-9z" />
        <path d="M4 11v8" />
        <path d="M13 11v8" />
        <path d="M8 20v-5" />
        <path d="M18 5c2 0 3 2 3 5v5h-6" />
        <path d="M19 15c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3z" />
        <path d="M7 15c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3z" />
    </svg>
);

export default GovernmentSchemes;
