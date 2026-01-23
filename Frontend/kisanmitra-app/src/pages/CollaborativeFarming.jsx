import React, { useState } from 'react';
import {
    Tractor,
    Users,
    MapPin,
    Filter,
    Star,
    Layers,
    Mic,
    RefreshCcw,
    Clock,
    ArrowRight
} from 'lucide-react';
import ActivePoolDashboard from '../components/ActivePoolDashboard';
import EquipmentRentalDetails from '../components/EquipmentRentalDetails';
import RentalConfirmation from '../components/RentalConfirmation';
import LandPoolingOverview from '../components/LandPoolingOverview';
import LandPoolingList from '../components/LandPoolingList';
import LandPoolDetails from '../components/LandPoolDetails';
import MapComponent from '../components/MapComponent';
import '../styles/global.css';

const CollaborativeFarming = () => {
    const [activeTab, setActiveTab] = useState('equipment'); // equipment | land

    // Land Pooling Flow State
    const [poolingStage, setPoolingStage] = useState('overview'); // overview | list | details | dashboard
    const [selectedPool, setSelectedPool] = useState(null);

    // Equipment Rental Flow State
    const [bookingStage, setBookingStage] = useState('search'); // search | details
    const [selectedEquipment, setSelectedEquipment] = useState(null);
    const [showConfirmation, setShowConfirmation] = useState(false);
    const [currentBooking, setCurrentBooking] = useState(null);

    // ----- Handlers: Equipment Rental -----
    const handleSelectEquipment = (equipment) => {
        setSelectedEquipment(equipment);
        setBookingStage('details');
    };

    const handleBackToSearch = () => {
        setBookingStage('search');
        setSelectedEquipment(null);
    };

    const handleConfirmBooking = (bookingDetails) => {
        setCurrentBooking(bookingDetails);
        setShowConfirmation(true);
    };

    const handleFinalizeBooking = () => {
        setShowConfirmation(false);
        setBookingStage('search');
        setSelectedEquipment(null);
        setCurrentBooking(null);
    };

    // ----- Handlers: Land Pooling -----
    const handleJoinClick = () => setPoolingStage('list');
    const handleSelectPool = (pool) => {
        setSelectedPool(pool);
        setPoolingStage('details');
    };
    const handleJoinPool = () => setPoolingStage('dashboard');
    const handleBackToOverview = () => setPoolingStage('overview');
    const handleBackToList = () => {
        setPoolingStage('list');
        setSelectedPool(null);
    };
    const handleBackToDetails = () => setPoolingStage('details');

    // Render Logic for Land Pooling Tab
    const renderLandPoolingContent = () => {
        switch (poolingStage) {
            case 'overview': return <LandPoolingOverview onJoinClick={handleJoinClick} />;
            case 'list': return <LandPoolingList onSelectPool={handleSelectPool} />;
            case 'details': return <LandPoolDetails pool={selectedPool} onBack={handleBackToList} onJoin={handleJoinPool} />;
            case 'dashboard': return <ActivePoolDashboard onBack={handleBackToDetails} />;
            default: return <LandPoolingOverview onJoinClick={handleJoinClick} />;
        }
    };

    return (
        <div style={{ backgroundColor: '#F9FBF4', minHeight: 'calc(100vh - 60px)', padding: '24px', maxWidth: '1400px', margin: '0 auto' }}>
            {/* Conditional Rental Confirmation Overlay */}
            {showConfirmation && currentBooking && (
                <RentalConfirmation
                    bookingDetails={currentBooking}
                    onFinalize={handleFinalizeBooking}
                    onClose={() => setShowConfirmation(false)}
                />
            )}

            {/* HEADER & TABS - RESTORED TO ORIGINAL CLEAN DESIGN */}
            {!(activeTab === 'equipment' && bookingStage === 'details') &&
                !(activeTab === 'land' && (poolingStage === 'details' || poolingStage === 'dashboard')) && (
                    <>
                        <div style={{ marginBottom: '24px' }}>
                            <h2 style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--color-text-dark)', marginBottom: '8px' }}>Collaborative Farming</h2>
                            <p style={{ color: 'var(--color-text-muted)', fontSize: '1.1rem' }}>Share resources to reduce costs and increase profit.</p>
                        </div>

                        <div style={{
                            display: 'flex',
                            width: 'fit-content',
                            backgroundColor: '#EAEAEA',
                            borderRadius: '12px',
                            padding: '4px',
                            marginBottom: '32px'
                        }}>
                            <button
                                onClick={() => setActiveTab('equipment')}
                                style={{
                                    padding: '10px 30px',
                                    borderRadius: '10px',
                                    backgroundColor: activeTab === 'equipment' ? 'white' : 'transparent',
                                    color: activeTab === 'equipment' ? 'var(--color-primary-green)' : 'var(--color-text-muted)',
                                    fontWeight: '600',
                                    boxShadow: activeTab === 'equipment' ? '0 2px 4px rgba(0,0,0,0.05)' : 'none',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '8px'
                                }}
                            >
                                <Tractor size={18} /> Equipment Rental
                            </button>
                            <button
                                onClick={() => setActiveTab('land')}
                                style={{
                                    padding: '10px 30px',
                                    borderRadius: '10px',
                                    backgroundColor: activeTab === 'land' ? 'white' : 'transparent',
                                    color: activeTab === 'land' ? 'var(--color-primary-green)' : 'var(--color-text-muted)',
                                    fontWeight: '600',
                                    boxShadow: activeTab === 'land' ? '0 2px 4px rgba(0,0,0,0.05)' : 'none',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '8px'
                                }}
                            >
                                <Users size={18} /> Land Pooling
                            </button>
                        </div>
                    </>
                )}

            {/* CONTENT RENDER */}
            {activeTab === 'equipment' ? (
                bookingStage === 'details' ? (
                    <EquipmentRentalDetails
                        equipment={selectedEquipment}
                        onBack={handleBackToSearch}
                        onConfirm={handleConfirmBooking}
                    />
                ) : (
                    <EquipmentRentalSection onSelectEquipment={handleSelectEquipment} />
                )
            ) : (
                renderLandPoolingContent()
            )}

            {/* FLOATING VOICE ASSIST */}
            <div style={{
                position: 'fixed',
                bottom: '30px',
                right: '30px',
                backgroundColor: 'var(--color-primary-green)',
                color: 'white',
                padding: '14px 24px',
                borderRadius: '40px',
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                boxShadow: '0 8px 20px rgba(76, 175, 80, 0.3)',
                cursor: 'pointer',
                zIndex: 1000
            }}>
                <Mic size={20} />
                <span style={{ fontWeight: '600' }}>Voice Assist</span>
            </div>
        </div>
    );
};

const EquipmentRentalSection = ({ onSelectEquipment }) => {
    return (
        <div>
            {/* Hero & Map Grid - RESTORED TO PROPER DESIGN */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: '1.8fr 1fr',
                gap: '24px',
                marginBottom: '24px'
            }}>
                {/* Hero Card */}
                <div style={{
                    position: 'relative',
                    borderRadius: '24px',
                    overflow: 'hidden',
                    height: '350px',
                    boxShadow: '0 4px 15px rgba(0,0,0,0.05)'
                }}>
                    <img
                        src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&q=80&w=1000"
                        alt="Farming Banner"
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                    />
                    <div style={{
                        position: 'absolute',
                        inset: 0,
                        background: 'linear-gradient(to top, rgba(0,0,0,0.4), transparent)',
                        display: 'flex',
                        alignItems: 'flex-end',
                        padding: '40px'
                    }}>
                        <h2 style={{ fontSize: '2.5rem', fontWeight: 'bold', color: 'white', maxWidth: '70%', lineHeight: '1.2' }}>
                            Connecting Farmers, Growing Together
                        </h2>
                    </div>
                </div>

                {/* Map Card */}
                <div style={{ padding: '0', overflow: 'hidden', display: 'flex', flexDirection: 'column', backgroundColor: 'white', borderRadius: '24px', boxShadow: '0 4px 15px rgba(0,0,0,0.05)' }}>
                    <div style={{ flex: 1, position: 'relative' }}>
                        <MapComponent
                            lat={30.9010}
                            lon={75.8573}
                            height="100%"
                            zoom={12}
                            markers={[
                                { lat: 30.91, lon: 75.85, popupText: "Tractor (2.5 km)" },
                                { lat: 30.89, lon: 75.87, popupText: "Harvester (5.0 km)" }
                            ]}
                        />
                        <div style={{
                            position: 'absolute',
                            top: '16px',
                            right: '16px',
                            backgroundColor: 'white',
                            padding: '8px',
                            borderRadius: '10px',
                            boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
                            cursor: 'pointer'
                        }}>
                            <Filter size={20} color="var(--color-primary-green)" />
                        </div>
                    </div>
                    <div style={{
                        padding: '16px 20px',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        backgroundColor: 'white',
                        borderTop: '1px solid #F0F0F0'
                    }}>
                        <span style={{ fontSize: '0.95rem', fontWeight: '600', color: 'var(--color-text-dark)' }}>Show Weather Overlay</span>
                        <div style={{ width: '40px', height: '20px', backgroundColor: '#E0E0E0', borderRadius: '10px', position: 'relative' }}>
                            <div style={{ width: '16px', height: '16px', backgroundColor: 'white', borderRadius: '50%', position: 'absolute', top: '2px', left: '2px' }} />
                        </div>
                    </div>
                </div>
            </div>

            {/* Viewing Near Status Indicator */}
            <div style={{
                backgroundColor: '#E3F2FD',
                color: '#1565C0',
                padding: '10px 20px',
                borderRadius: '30px',
                marginBottom: '32px',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: '0.9rem',
                fontWeight: '600'
            }}>
                <MapPin size={16} /> Viewing equipment near you
            </div>

            {/* List Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--color-text-dark)' }}>Available Nearby</h3>
                <button style={{
                    backgroundColor: 'var(--color-primary-green)',
                    color: 'white',
                    padding: '10px 24px',
                    borderRadius: '12px',
                    fontWeight: 'bold',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px'
                }}>
                    <Tractor size={20} /> Rent Now
                </button>
            </div>

            {/* Equipment List - ACCURATE IMAGES AND CONTENT */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <EquipmentCard
                    image="/assets/tractor.png"
                    name="Mahindra Novo 755 DI"
                    rating="4.8"
                    price="₹800/hr"
                    distance="2.5 km"
                    owner="Surjit Singh"
                    onClick={() => onSelectEquipment({ name: "Mahindra Novo 755 DI", price: "₹800/hr", rating: "4.8", owner: "Surjit Singh", distance: "2.5 km" })}
                />
                <EquipmentCard
                    image="/assets/harvester.png"
                    name="Class Dominator Harvester"
                    rating="4.9"
                    price="₹2,500/acre"
                    distance="5.0 km"
                    owner="Gurpreet Farms"
                    onClick={() => onSelectEquipment({ name: "Class Dominator Harvester", price: "₹2,500/acre", rating: "4.9", owner: "Gurpreet Farms", distance: "5.0 km" })}
                />
                <EquipmentCard
                    image="/assets/drone.png"
                    name="DJI Agras T30 Spraying Drone"
                    rating="4.7"
                    price="₹1,200/day"
                    distance="3.2 km"
                    owner="Village Cooperative"
                    onClick={() => onSelectEquipment({ name: "DJI Agras T30 Spraying Drone", price: "₹1,200/day", rating: "4.7", owner: "Village Cooperative", distance: "3.2 km" })}
                />
            </div>
        </div>
    );
};

const EquipmentCard = ({ image, name, rating, price, distance, owner, onClick }) => (
    <div
        onClick={onClick}
        style={{
            backgroundColor: 'white',
            borderRadius: '16px',
            padding: '16px',
            display: 'flex',
            alignItems: 'center',
            gap: '24px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
            cursor: 'pointer',
            transition: 'transform 0.2s ease',
            border: '1px solid transparent'
        }}
        onMouseEnter={(e) => { e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.borderColor = 'var(--color-primary-green)'; }}
        onMouseLeave={(e) => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.borderColor = 'transparent'; }}
    >
        <div style={{ width: '150px', height: '100px', borderRadius: '12px', overflow: 'hidden', backgroundColor: '#F8F9F3', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <img src={image} style={{ width: '90%', height: '90%', objectFit: 'contain' }} alt={name} />
        </div>
        <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                    <h4 style={{ margin: 0, fontSize: '1.25rem', fontWeight: 'bold', color: 'var(--color-text-dark)' }}>{name}</h4>
                    <p style={{ margin: '4px 0 0 0', color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>Owned by: {owner}</p>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#FBC02D', fontWeight: 'bold' }}>
                    <Star size={18} fill="#FBC02D" /> {rating}
                </div>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '16px', alignItems: 'center' }}>
                <div style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <MapPin size={16} color="var(--color-primary-green)" /> {distance} away
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <span style={{ fontWeight: 'bold', color: 'var(--color-primary-green)', fontSize: '1.2rem' }}>{price}</span>
                    <button style={{
                        padding: '8px 20px',
                        backgroundColor: 'var(--color-primary-green)',
                        color: 'white',
                        borderRadius: '8px',
                        fontWeight: 'bold',
                        fontSize: '0.9rem',
                        border: 'none'
                    }}>
                        Rent Now
                    </button>
                </div>
            </div>
        </div>
    </div>
);

export default CollaborativeFarming;
