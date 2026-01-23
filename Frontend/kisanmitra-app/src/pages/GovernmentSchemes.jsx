import React, { useState, useEffect } from 'react';
import {
    ShieldCheck, Landmark, Handshake, Sprout, Sparkles,
    IndianRupee, Info, Eye, Umbrella, CheckCircle,
    ArrowRight, CreditCard, FileSignature, Mountain, Ban,
    Search, Filter, ExternalLink, Loader2
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

    const [activeFilter, setActiveFilter] = useState("All Schemes");
    const [schemes, setSchemes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [stats, setStats] = useState({ total: 0, new: 0 });

    useEffect(() => {
        fetchSchemes();
    }, []);

    const fetchSchemes = async () => {
        try {
            setLoading(true);
            // Fetching all schemes initially
            const res = await fetch('/api/v1/schemes');
            if (!res.ok) throw new Error("Failed to fetch schemes");
            const data = await res.json();

            setSchemes(data.schemeCards || []);
            setStats({
                total: data.totalSchemes || 0,
                new: data.newSchemesCount || 0
            });
        } catch (error) {
            console.error("Error loading schemes:", error);
            // Fallback to empty or error state
        } finally {
            setLoading(false);
        }
    };

    // --- Filtering Logic (Frontend Side for Demo Smoothness) ---
    const getFilteredSchemes = () => {
        if (activeFilter === "All Schemes") return schemes;

        const lowerFilter = activeFilter.toLowerCase();
        return schemes.filter(s => {
            const cat = (s.categoryDisplay || "").toLowerCase();
            const scope = (s.scope || "").toLowerCase();
            const desc = (s.description || "").toLowerCase();
            const name = (s.schemeName || "").toLowerCase();

            if (activeFilter.includes("Crop") && (cat.includes("crop") || name.includes("crop") || desc.includes("crop"))) return true;
            if (activeFilter.includes("Location") && (scope.includes("state") || scope.includes("district"))) return true;
            if (activeFilter.includes("Subsidy") && (cat.includes("subsidy") || desc.includes("subsidy"))) return true;
            if (activeFilter.includes("Insurance") && (cat.includes("insurance") || desc.includes("insurance") || name.includes("bima"))) return true;
            if (activeFilter.includes("Equipment") && (cat.includes("equipment") || cat.includes("machin") || desc.includes("equipment") || desc.includes("tractor") || desc.includes("machine"))) return true;

            // Fallback loose match
            return cat.includes(lowerFilter.split(' ')[1]?.toLowerCase() || "xyz");
        });
    };

    const filteredList = getFilteredSchemes();
    const recommendedScheme = schemes.find(s => s.categoryDisplay?.includes("Subsidy") || s.schemeName.includes("PM-Kisan")) || schemes[0];

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
                        {stats.new > 0 && <span style={{ display: 'block', marginTop: '8px', color: colors.accentOchre, fontWeight: 'bold' }}>✨ {stats.new} new schemes added recently!</span>}
                    </p>
                    <button onClick={() => document.getElementById('scheme-list').scrollIntoView({ behavior: 'smooth' })} style={{
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
                        <button
                            key={index}
                            onClick={() => setActiveFilter(filter)}
                            style={{
                                whiteSpace: 'nowrap',
                                padding: '10px 20px',
                                borderRadius: '24px',
                                backgroundColor: activeFilter === filter ? colors.textMain : 'white',
                                color: activeFilter === filter ? 'white' : colors.textSecondary,
                                border: activeFilter === filter ? 'none' : '1px solid #E6DCC8',
                                fontWeight: 'bold', fontSize: '0.9rem',
                                cursor: 'pointer',
                                display: 'flex', alignItems: 'center', gap: '6px',
                                transition: 'all 0.2s'
                            }}>
                            {filter}
                        </button>
                    ))}
                </div>
            </div>

            {loading ? (
                <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
                    <Loader2 className="spin" size={40} color={colors.primary} />
                </div>
            ) : (
                <>
                    {/* Recommended Section (Dynamic) */}
                    {recommendedScheme && activeFilter === "All Schemes" && (
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
                                                <h4 style={{ fontSize: '1.5rem', fontWeight: '900', color: colors.textMain, margin: 0 }}>{recommendedScheme.schemeName}</h4>
                                                <span style={{ fontSize: '0.75rem', fontWeight: 'bold', backgroundColor: colors.accentOchre, color: 'white', padding: '2px 8px', borderRadius: '4px' }}>Top Match</span>
                                            </div>
                                            <p style={{ fontSize: '1.1rem', color: colors.textSecondary, marginBottom: '12px', lineHeight: 1.5 }}>
                                                {recommendedScheme.description}
                                            </p>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', color: colors.textSecondary, backgroundColor: colors.cardBeige, padding: '6px 12px', borderRadius: '8px', width: 'fit-content' }}>
                                                <Info size={16} /> <span>{recommendedScheme.benefits}</span>
                                            </div>
                                        </div>
                                    </div>
                                    <button
                                        onClick={() => recommendedScheme.officialLink && window.open(recommendedScheme.officialLink, '_blank')}
                                        style={{
                                            whiteSpace: 'nowrap',
                                            padding: '14px 28px', backgroundColor: colors.accentOchre,
                                            color: 'white', borderRadius: '12px',
                                            fontSize: '1rem', fontWeight: 'bold', border: 'none',
                                            display: 'flex', alignItems: 'center', gap: '8px',
                                            cursor: 'pointer', boxShadow: '0 4px 12px rgba(217, 165, 76, 0.2)'
                                        }}>
                                        Apply Now <ExternalLink size={20} />
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Available Grid */}
                    <div id="scheme-list">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                            <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: colors.textMain }}>Available Schemes</h3>
                            <span style={{ fontSize: '0.9rem', color: colors.textSecondary, fontWeight: '500' }}>Showing {filteredList.length} results</span>
                        </div>

                        {filteredList.length === 0 ? (
                            <div style={{ textAlign: 'center', padding: '40px', color: colors.textSecondary }}>
                                No schemes found for this category.
                            </div>
                        ) : (
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
                                {filteredList.map((scheme) => (
                                    <SchemeCard
                                        key={scheme.schemeId}
                                        title={scheme.schemeName}
                                        desc={scheme.description}
                                        benefits={scheme.benefits}
                                        // Dynamic Icon Logic based on category/name
                                        icon={getIconForScheme(scheme)}
                                        iconColor={getColorForScheme(scheme).color}
                                        iconBg={getColorForScheme(scheme).bg}
                                        tag={scheme.isNew ? "New Arrival" : (scheme.scope || "Eligible")}
                                        tagIcon={scheme.isNew ? Sparkles : CheckCircle}
                                        tagColor={scheme.isNew ? "red" : "green"}
                                        footerLabel={scheme.categoryDisplay}
                                        footerAction="View Official Site"
                                        link={scheme.officialLink}
                                        borderHoverColor={colors.primary}
                                    />
                                ))}
                            </div>
                        )}
                    </div>
                </>
            )}
        </div>
    );
};

// --- Helper Functions ---
const getIconForScheme = (scheme) => {
    const name = (scheme.schemeName || "").toLowerCase();
    const cat = (scheme.categoryDisplay || "").toLowerCase();

    if (name.includes("soil")) return Mountain;
    if (name.includes("credit") || name.includes("kcc")) return CreditCard;
    if (name.includes("insur") || name.includes("bima")) return Umbrella;
    if (name.includes("tractor") || name.includes("mech")) return Tractor;
    if (name.includes("irrig")) return Sprout; // Using Sprout as proxy for irrigation/water if dropped doesn't exist? Actually Droplets exists
    // Let's use generic if not matched
    return Landmark;
};

const getColorForScheme = (scheme) => {
    const name = (scheme.schemeName || "").toLowerCase();
    if (name.includes("soil")) return { color: "#E65100", bg: "#FFF3E0" }; // Orange
    if (name.includes("credit")) return { color: "#1565C0", bg: "#E3F2FD" }; // Blue
    if (name.includes("insur")) return { color: "#2E7D32", bg: "#E8F5E9" }; // Green
    return { color: "#616161", bg: "#F5F5F5" }; // Grey default
};

const SchemeCard = ({ title, desc, icon: Icon, iconColor, iconBg, tag, tagIcon: TagIcon, tagColor, footerLabel, footerAction, isClosed, borderHoverColor, link }) => {

    const tagStyles = {
        green: { bg: '#E8F5E9', text: '#2E7D32', border: '#C8E6C9' },
        gray: { bg: '#F5F5F5', text: '#616161', border: '#E0E0E0' },
        red: { bg: '#FFEBEE', text: '#C62828', border: '#FFCDD2' }
    };
    const currentTag = tagStyles[tagColor] || tagStyles.green;

    const handleCardClick = () => {
        if (link) {
            window.open(link, '_blank', 'noopener,noreferrer');
        } else {
            alert("Official link not available for this scheme.");
        }
    };

    return (
        <div
            onClick={handleCardClick}
            className="hover-scale"
            style={{
                backgroundColor: 'white', borderRadius: '16px', padding: '24px',
                border: '1px solid #E6DCC8', display: 'flex', flexDirection: 'column',
                cursor: 'pointer', transition: 'all 0.2s', opacity: isClosed ? 0.8 : 1,
                minHeight: '280px'
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

            <div style={{ marginBottom: '16px', flex: 1 }}>
                <h4 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#423E37', marginBottom: '8px', lineHeight: 1.3 }}>{title}</h4>
                <p style={{ fontSize: '0.9rem', color: '#6B6358', lineHeight: 1.5, display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
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
                    {footerAction} {!isClosed && <ExternalLink size={16} />}
                </span>
            </div>
        </div>
    );
};

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
