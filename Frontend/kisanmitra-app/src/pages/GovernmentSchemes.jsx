import React, { useState, useEffect } from 'react';
import {
    ShieldCheck, Landmark, Handshake, Sprout, Sparkles,
    IndianRupee, Info, Eye, Umbrella, CheckCircle,
    ArrowRight, CreditCard, FileSignature, Mountain, Ban,
    Search, Filter
} from 'lucide-react';
import '../styles/global.css';
import { getSchemes } from '../services/schemesService';
import { getErrorMessage } from '../services/api';

const GovernmentSchemes = () => {
    const [schemes, setSchemes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [activeFilter, setActiveFilter] = useState('all');

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

    // Fetch schemes on mount
    useEffect(() => {
        loadSchemes();
    }, []);

    const loadSchemes = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await getSchemes();
            if (response.success && response.schemes) {
                setSchemes(response.schemes);
            }
        } catch (err) {
            setError(getErrorMessage(err));
            console.error('Failed to load schemes:', err);
        } finally {
            setLoading(false);
        }
    };

    const filterCategories = [
        { id: 'all', label: "All Schemes" },
        { id: 'crop', label: "🌱 Crop Based" },
        { id: 'location', label: "📍 Location Based" },
        { id: 'subsidy', label: "💰 Subsidy" },
        { id: 'insurance', label: "🛡️ Insurance" },
        { id: 'equipment', label: "🚜 Equipment" }
    ];

    // Get recommended scheme (first match with is_top_recommendation)
    const recommendedScheme = schemes.find(s => s.is_top_recommendation);

    // Filter schemes (excluding recommended from main list)
    const filteredSchemes = schemes.filter(s => {
        if (s.is_top_recommendation) return false; // Don't show in main list
        if (activeFilter === 'all') return true;
        return s.category && s.category.toLowerCase().includes(activeFilter);
    });

    return (
        <div className="fade-in" style={{ paddingBottom: '80px', maxWidth: '1200px', margin: '0 auto' }}>

            {/* Loading State */}
            {loading && (
                <div style={{ textAlign: 'center', padding: '80px 20px', color: colors.textSecondary }}>
                    <div className="spinner" style={{ margin: '0 auto 16px', width: '40px', height: '40px', border: `4px solid ${colors.cardBeige}`, borderTop: `4px solid ${colors.primary}`, borderRadius: '50%', animation: 'spin 1s linear infinite' }}></div>
                    <p>Loading schemes...</p>
                </div>
            )}

            {/* Error State */}
            {error && !loading && (
                <div style={{ textAlign: 'center', padding: '40px', backgroundColor: '#FFEBEE', borderRadius: '12px', color: '#C62828', marginBottom: '24px' }}>
                    <p style={{ marginBottom: '12px' }}>{error}</p>
                    <button onClick={loadSchemes} style={{ padding: '10px 20px', backgroundColor: colors.primary, color: 'white', borderRadius: '8px', fontWeight: 'bold', cursor: 'pointer' }}>
                        Retry
                    </button>
                </div>
            )}

            {/* Schemes Content */}
            {!loading && !error && (
                <>
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
                            {filterCategories.map((filter) => (
                                <button
                                    key={filter.id}
                                    onClick={() => setActiveFilter(filter.id)}
                                    style={{
                                        whiteSpace: 'nowrap',
                                        padding: '10px 20px',
                                        borderRadius: '24px',
                                        backgroundColor: activeFilter === filter.id ? colors.textMain : 'white',
                                        color: activeFilter === filter.id ? 'white' : colors.textSecondary,
                                        border: activeFilter === filter.id ? 'none' : '1px solid #E6DCC8',
                                        fontWeight: 'bold', fontSize: '0.9rem',
                                        cursor: 'pointer',
                                        display: 'flex', alignItems: 'center', gap: '6px'
                                    }}
                                >
                                    {filter.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Recommended Section */}
                    {recommendedScheme && (
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
                                                <h4 style={{ fontSize: '1.5rem', fontWeight: '900', color: colors.textMain, margin: 0 }}>{recommendedScheme.title}</h4>
                                                <span style={{ fontSize: '0.75rem', fontWeight: 'bold', backgroundColor: colors.accentOchre, color: 'white', padding: '2px 8px', borderRadius: '4px' }}>Top Match</span>
                                            </div>
                                            <p style={{ fontSize: '1.1rem', color: colors.textSecondary, marginBottom: '12px' }}>
                                                {recommendedScheme.benefit_amount && (
                                                    <><strong style={{ color: colors.textMain }}>{recommendedScheme.benefit_amount}</strong>{' - '}</>
                                                )}
                                                {recommendedScheme.description?.substring(0, 120)}...
                                            </p>
                                            {recommendedScheme.eligibility && recommendedScheme.eligibility.length > 0 && (
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', color: colors.textSecondary, backgroundColor: colors.cardBeige, padding: '6px 12px', borderRadius: '8px', width: 'fit-content' }}>
                                                    <Info size={16} /> <span>Eligibility: {recommendedScheme.eligibility[0]}</span>
                                                </div>
                                            )}
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
                    )}

                    {/* Available Grid */}
                    <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                            <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: colors.textMain }}>Available Schemes</h3>
                            <span style={{ fontSize: '0.9rem', color: colors.textSecondary, fontWeight: '500' }}>
                                Showing {filteredSchemes.length} result{filteredSchemes.length !== 1 ? 's' : ''}
                            </span>
                        </div>

                        {filteredSchemes.length === 0 ? (
                            <div style={{ textAlign: 'center', padding: '60px 20px', color: colors.textSecondary }}>
                                <Sprout size={48} style={{ marginBottom: '16px', opacity: 0.5 }} />
                                <p>No schemes found for the selected filter.</p>
                            </div>
                        ) : (
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
                                {filteredSchemes.map((scheme) => (
                                    <SchemeCardDynamic
                                        key={scheme.scheme_id || scheme.title}
                                        scheme={scheme}
                                        colors={colors}
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

// Dynamic scheme card from API data
const SchemeCardDynamic = ({ scheme, colors }) => {
    // Map category to icon and color
    const getCategoryIcon = (category) => {
        const cat = category?.toLowerCase() || '';
        if (cat.includes('insurance')) return { Icon: Umbrella, color: '#2E7D32', bg: '#E8F5E9' };
        if (cat.includes('loan') || cat.includes('credit')) return { Icon: CreditCard, color: '#1565C0', bg: '#E3F2FD' };
        if (cat.includes('subsidy')) return { Icon: IndianRupee, color: '#E65100', bg: '#FFF3E0' };
        if (cat.includes('advisory')) return { Icon: Mountain, color: '#00897B', bg: '#E0F2F1' };
        return { Icon: Sprout, color: '#558B2F', bg: '#F1F8E9' };
    };

    const { Icon, color: iconColor, bg: iconBg } = getCategoryIcon(scheme.category);
    const isActive = scheme.status?.toLowerCase() !== 'closed';

    return (
        <div className="hover-scale" style={{
            backgroundColor: 'white', borderRadius: '16px', padding: '24px',
            border: '1px solid #E6DCC8', display: 'flex', flexDirection: 'column',
            cursor: 'pointer', transition: 'all 0.2s', opacity: isActive ? 1 : 0.7
        }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                <div style={{
                    padding: '12px', borderRadius: '12px', backgroundColor: iconBg,
                    color: iconColor, display: 'flex', alignItems: 'center', justifyContent: 'center'
                }}>
                    <Icon size={28} />
                </div>
                {scheme.status && (
                    <div style={{
                        display: 'flex', alignItems: 'center', gap: '4px',
                        padding: '4px 10px', borderRadius: '20px',
                        backgroundColor: isActive ? '#E8F5E9' : '#FFEBEE',
                        color: isActive ? '#2E7D32' : '#C62828',
                        border: `1px solid ${isActive ? '#C8E6C9' : '#FFCDD2'}`,
                        fontSize: '0.75rem', fontWeight: 'bold'
                    }}>
                        {isActive ? <CheckCircle size={14} /> : <Ban size={14} />} {scheme.status}
                    </div>
                )}
            </div>

            <div style={{ marginBottom: '16px' }}>
                <h4 style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#423E37', marginBottom: '8px', lineHeight: 1.3 }}>
                    {scheme.title}
                </h4>
                <p style={{ fontSize: '0.9rem', color: '#6B6358', lineHeight: 1.5, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    {scheme.description}
                </p>
                {scheme.benefit_amount && (
                    <div style={{ marginTop: '8px', fontSize: '0.9rem', fontWeight: 'bold', color: colors.accentOchre }}>
                        Benefit: {scheme.benefit_amount}
                    </div>
                )}
            </div>

            <div style={{
                marginTop: 'auto', paddingTop: '16px', borderTop: '1px solid #E6DCC8',
                display: 'flex', justifyContent: 'space-between', alignItems: 'center'
            }}>
                <span style={{ fontSize: '0.75rem', fontWeight: 'bold', color: '#6B6358', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                    {scheme.category || 'Scheme'}
                </span>
                <span style={{
                    fontSize: '0.9rem', fontWeight: 'bold', color: isActive ? '#8FA892' : '#6B6358',
                    display: 'flex', alignItems: 'center', gap: '4px'
                }}>
                    {isActive ? 'View Details' : 'Closed'} {isActive && <ArrowRight size={16} />}
                </span>
            </div>
        </div>
    );
};

export default GovernmentSchemes;
