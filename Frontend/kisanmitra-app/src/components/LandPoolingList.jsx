import React from 'react';
import {
    Filter,
    Plus,
    MapPin,
    Users,
    Leaf,
    Truck,
    Store,
    Settings,
    ArrowRight,
    Wheat
} from 'lucide-react';
import '../styles/global.css';
import MapComponent from './MapComponent';

const LandPoolingList = ({ onSelectPool }) => {
    return (
        <div className="fade-in">
            {/* Header / Filter Toolbar */}
            <div style={{ marginBottom: '24px', display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between' }}>
                <div>
                    <h2 style={{ fontSize: '2rem', fontWeight: '900', margin: 0, color: 'var(--color-text-dark)' }}>Available Land Pools</h2>
                    <p style={{ fontSize: '1.1rem', color: 'var(--color-text-muted)', marginTop: '8px', maxWidth: '600px' }}>Join collaborative farming groups in your area to share resources, reduce costs, and access bulk buyers.</p>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                    <button style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '8px 16px',
                        backgroundColor: 'white',
                        border: '1px solid var(--color-border)',
                        borderRadius: '8px',
                        fontWeight: 'bold',
                        color: 'var(--color-text-dark)'
                    }}>
                        <Filter size={18} /> Filter
                    </button>
                    <button style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '8px 16px',
                        backgroundColor: 'var(--color-text-dark)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        fontWeight: 'bold'
                    }}>
                        <Plus size={18} /> Create Group
                    </button>
                </div>
            </div>

            {/* MAP VIEW INTEGRATION */}
            <div style={{ marginBottom: '32px' }}>
                <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
                    <MapComponent
                        lat={30.9010}
                        lon={75.8573}
                        height="250px"
                        zoom={11}
                        markers={[
                            { lat: 30.91, lon: 75.85, popupText: "Village Wheat Cooperative (45 Acres)" },
                            { lat: 30.88, lon: 75.90, popupText: "Organic Veggies Collective (12 Acres)" },
                            { lat: 30.95, lon: 75.80, popupText: "Paddy Field Alliance (85 Acres)" }
                        ]}
                    />
                    <div style={{ padding: '8px 16px', borderTop: '1px solid var(--color-border)', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>
                        <MapPin size={16} color="var(--color-primary-green)" /> Found 3 active pools in Ludhiana District
                    </div>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '24px' }}>

                {/* Pool Card 1 */}
                <PoolCard
                    tag="Active"
                    tagColor="green"
                    title="Village Wheat Cooperative"
                    location="Ludhiana North, Punjab"
                    totalLand="45 Acres"
                    crop="Wheat"
                    benefit="Bulk Buyer Targeted"
                    benefitIcon={Truck}
                    onClick={() => onSelectPool({
                        id: 1,
                        name: "Village Wheat Cooperative",
                        location: "Ludhiana North, Punjab",
                        totalLand: "45 Acres",
                        crop: "Wheat"
                    })}
                />

                {/* Pool Card 2 */}
                <PoolCard
                    tag="Filling Fast"
                    tagColor="orange"
                    title="Organic Veggies Collective"
                    location="Samrala, Punjab"
                    totalLand="12 Acres"
                    crop="Mixed Veg"
                    benefit="Direct Retail Access"
                    benefitIcon={Store}
                    onClick={() => onSelectPool({
                        id: 2,
                        name: "Organic Veggies Collective",
                        location: "Samrala, Punjab",
                        totalLand: "12 Acres",
                        crop: "Mixed Veg"
                    })}
                />

                {/* Pool Card 3 */}
                <PoolCard
                    tag="New"
                    tagColor="blue"
                    title="Paddy Field Alliance"
                    location="Khanna District"
                    totalLand="85 Acres"
                    crop="Rice"
                    benefit="Shared Machinery"
                    benefitIcon={Settings}
                    onClick={() => onSelectPool({
                        id: 3,
                        name: "Paddy Field Alliance",
                        location: "Khanna District",
                        totalLand: "85 Acres",
                        crop: "Rice"
                    })}
                />

                {/* New Pool CTA Card */}
                <button style={{
                    backgroundColor: 'transparent',
                    border: '2px dashed var(--color-border)',
                    borderRadius: '16px',
                    padding: '24px',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: '100%',
                    minHeight: '300px',
                    cursor: 'pointer',
                    transition: 'all 0.2s'
                }}
                    className="hover-border-primary"
                >
                    <div style={{
                        width: '64px',
                        height: '64px',
                        borderRadius: '50%',
                        backgroundColor: 'var(--color-card-brown)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        marginBottom: '16px'
                    }}>
                        <Plus size={32} color="var(--color-text-muted)" />
                    </div>
                    <div style={{ textAlign: 'center' }}>
                        <h3 style={{ fontSize: '1.2rem', fontWeight: 'bold', marginBottom: '4px', color: 'var(--color-text-dark)' }}>Start a New Pool</h3>
                        <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>Can't find a suitable group?<br />Start one for your village.</p>
                    </div>
                </button>

            </div>
        </div>
    );
};

const PoolCard = ({ tag, tagColor, title, location, totalLand, crop, benefit, benefitIcon: BenefitIcon, onClick }) => {
    const getTagStyles = (color) => {
        const styles = {
            green: { bg: '#E8F5E9', text: '#2E7D32' },
            orange: { bg: '#FFF3E0', text: '#EF6C00' },
            blue: { bg: '#E3F2FD', text: '#1565C0' },
        };
        return styles[color] || styles.green;
    };

    const tagStyle = getTagStyles(tagColor);

    return (
        <div className="card" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
                <div>
                    <div style={{ marginBottom: '4px' }}>
                        <span style={{
                            padding: '2px 8px',
                            borderRadius: '4px',
                            fontSize: '0.7rem',
                            fontWeight: 'bold',
                            textTransform: 'uppercase',
                            backgroundColor: tagStyle.bg,
                            color: tagStyle.text
                        }}>
                            {tag}
                        </span>
                    </div>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: 'bold', margin: '0 0 4px 0', color: 'var(--color-text-dark)' }}>{title}</h3>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>
                        <MapPin size={16} /> {location}
                    </div>
                </div>
                <div style={{
                    width: '40px',
                    height: '40px',
                    borderRadius: '50%',
                    backgroundColor: 'white',
                    border: '1px solid var(--color-border)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--color-primary-green)'
                }}>
                    <Users size={20} />
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '20px' }}>
                <div style={{ backgroundColor: 'rgba(255,255,255,0.6)', padding: '12px', borderRadius: '8px', border: '1px solid rgba(0,0,0,0.05)' }}>
                    <p style={{ fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--color-text-muted)', textTransform: 'uppercase', marginBottom: '4px' }}>TOTAL LAND</p>
                    <p style={{ fontSize: '1.1rem', fontWeight: '900', margin: 0 }}>{totalLand}</p>
                </div>
                <div style={{ backgroundColor: 'rgba(255,255,255,0.6)', padding: '12px', borderRadius: '8px', border: '1px solid rgba(0,0,0,0.05)' }}>
                    <p style={{ fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--color-text-muted)', textTransform: 'uppercase', marginBottom: '4px' }}>CROP</p>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                        {crop === 'Wheat' ? (
                            <Wheat size={16} color="var(--color-accent-ochre)" />
                        ) : (
                            <Leaf size={16} color="var(--color-accent-ochre)" />
                        )}
                        <p style={{ fontSize: '1.1rem', fontWeight: '900', margin: 0 }}>{crop}</p>
                    </div>
                </div>
            </div>

            <div style={{
                backgroundColor: 'white',
                borderRadius: '8px',
                padding: '12px',
                marginBottom: '24px',
                border: '1px solid var(--color-border)',
                display: 'flex',
                alignItems: 'center',
                gap: '12px'
            }}>
                <BenefitIcon size={20} color="var(--color-accent-ochre)" />
                <div>
                    <p style={{ fontSize: '0.75rem', fontWeight: '500', color: 'var(--color-text-muted)', marginBottom: '0' }}>Key Benefit</p>
                    <p style={{ fontSize: '0.9rem', fontWeight: 'bold', margin: 0 }}>{benefit}</p>
                </div>
            </div>

            <button
                onClick={onClick}
                style={{
                    marginTop: 'auto',
                    width: '100%',
                    padding: '14px',
                    backgroundColor: 'var(--color-primary-green)',
                    color: 'white',
                    borderRadius: '12px',
                    fontSize: '1rem',
                    fontWeight: 'bold',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '8px'
                }}
            >
                Join Group <ArrowRight size={20} />
            </button>
        </div>
    );
};

export default LandPoolingList;
