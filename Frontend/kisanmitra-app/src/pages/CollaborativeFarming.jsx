import React, { useState } from 'react';
import {
    Tractor,
    Users,
    MapPin,
    Search,
    Filter,
    ArrowRight,
    PhoneCall,
    Star,
    Share2,
    Calendar
} from 'lucide-react';
import ActivePoolDashboard from '../components/ActivePoolDashboard';
import EquipmentRentalDetails from '../components/EquipmentRentalDetails';
import RentalConfirmation from '../components/RentalConfirmation';
import LandPoolingOverview from '../components/LandPoolingOverview';
import LandPoolingList from '../components/LandPoolingList';
import LandPoolDetails from '../components/LandPoolDetails';
import '../styles/global.css';
import MapComponent from '../components/MapComponent';

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

    // 1. Overview -> List
    const handleJoinClick = () => {
        setPoolingStage('list');
    };

    // 2. List -> Details
    const handleSelectPool = (pool) => {
        setSelectedPool(pool);
        setPoolingStage('details');
    };

    // 3. Details -> Dashboard (Join)
    const handleJoinPool = () => {
        // Here we would have a confirmation, but for now go straight to dashboard
        setPoolingStage('dashboard');
    };

    // Back Navigation
    const handleBackToOverview = () => setPoolingStage('overview');
    const handleBackToList = () => {
        setPoolingStage('list');
        setSelectedPool(null);
    };
    const handleBackToDetails = () => setPoolingStage('details');


    // Render Logic for Land Pooling Tab
    const renderLandPoolingContent = () => {
        switch (poolingStage) {
            case 'overview':
                return <LandPoolingOverview onJoinClick={handleJoinClick} />;
            case 'list':
                return <LandPoolingList onSelectPool={handleSelectPool} />;
            case 'details':
                return <LandPoolDetails pool={selectedPool} onBack={handleBackToList} onJoin={handleJoinPool} />;
            case 'dashboard':
                return <ActivePoolDashboard onBack={handleBackToDetails} />;
            default:
                return <LandPoolingOverview onJoinClick={handleJoinClick} />;
        }
    };

    return (
        <div style={{ paddingBottom: '80px' }}>
            {/* Conditional Rental Confirmation Overlay */}
            {showConfirmation && currentBooking && (
                <RentalConfirmation
                    bookingDetails={currentBooking}
                    onFinalize={handleFinalizeBooking}
                    onClose={() => setShowConfirmation(false)}
                />
            )}

            {/* HEADER & TABS (Only show if NOT in deep detail views that should take over screen) */}
            {/* Note: In this design, we keep the header/tabs visible for Overview/List/Search, but maybe hide for Details/Dashboard */}

            {/* Logic: Hide Tabs/Header if:
                - Active Tab is Equipment AND Stage is 'details'
                - Active Tab is Land AND Stage is 'details' OR 'dashboard'
            */}
            {!(activeTab === 'equipment' && bookingStage === 'details') &&
                !(activeTab === 'land' && (poolingStage === 'details' || poolingStage === 'dashboard')) && (
                    <>
                        <div style={{ marginBottom: '24px' }}>
                            <h2 style={{ fontSize: '1.5rem', marginBottom: '8px' }}>Collaborative Farming</h2>
                            <p style={{ color: 'var(--color-text-muted)' }}>Share resources to reduce costs and increase profit.</p>
                        </div>

                        <div style={{
                            display: 'flex',
                            backgroundColor: '#EAEAEA',
                            borderRadius: '12px',
                            padding: '4px',
                            marginBottom: '24px'
                        }}>
                            <button
                                onClick={() => setActiveTab('equipment')}
                                style={{
                                    flex: 1,
                                    padding: '12px',
                                    borderRadius: '10px',
                                    backgroundColor: activeTab === 'equipment' ? 'white' : 'transparent',
                                    color: activeTab === 'equipment' ? 'var(--color-primary-green)' : 'var(--color-text-muted)',
                                    fontWeight: '600',
                                    boxShadow: activeTab === 'equipment' ? '0 2px 4px rgba(0,0,0,0.1)' : 'none',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    gap: '8px'
                                }}
                            >
                                <Tractor size={20} /> Equipment Rental
                            </button>
                            <button
                                onClick={() => setActiveTab('land')}
                                style={{
                                    flex: 1,
                                    padding: '12px',
                                    borderRadius: '10px',
                                    backgroundColor: activeTab === 'land' ? 'white' : 'transparent',
                                    color: activeTab === 'land' ? 'var(--color-primary-green)' : 'var(--color-text-muted)',
                                    fontWeight: '600',
                                    boxShadow: activeTab === 'land' ? '0 2px 4px rgba(0,0,0,0.1)' : 'none',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    gap: '8px'
                                }}
                            >
                                <Users size={20} /> Land Pooling
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
        </div>
    );
};

/* -------------------------------------------------------------------------- */
/* EQUIPMENT RENTAL SECTION                                                    */
/* -------------------------------------------------------------------------- */

const EquipmentRentalSection = ({ onSelectEquipment }) => {
    return (
        <div>
            {/* Search Bar */}
            <div className="card" style={{ padding: '12px', display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                <Search size={20} color="var(--color-text-muted)" />
                <input
                    type="text"
                    placeholder="Find tractor, harvester, sprayer..."
                    style={{
                        border: 'none',
                        outline: 'none',
                        fontSize: '1rem',
                        flex: 1,
                        backgroundColor: 'transparent'
                    }}
                />
                <button style={{ padding: '8px', backgroundColor: 'var(--color-bg-beige)', borderRadius: '8px' }}>
                    <Filter size={20} />
                </button>
            </div>

            {/* Map Placeholder - REPLACED WITH REAL MAP */}
            <div className="card" style={{ padding: '0', overflow: 'hidden', marginBottom: '20px', border: '1px solid var(--color-border)' }}>
                <MapComponent
                    lat={30.9010}
                    lon={75.8573}
                    height="200px"
                    zoom={12}
                    markers={[
                        { lat: 30.91, lon: 75.85, popupText: "Mahindra Tractor (2.5 km)" },
                        { lat: 30.89, lon: 75.87, popupText: "Combine Harvester (5 km)" },
                        { lat: 30.92, lon: 75.82, popupText: "Spraying Drone" }
                    ]}
                />
                <div style={{ padding: '8px 12px', background: '#E3F2FD', color: '#1565C0', fontSize: '0.9rem', fontWeight: '500', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <MapPin size={16} /> Viewing equipment near you
                </div>
            </div>

            {/* Equipment List */}
            <h3 style={{ marginBottom: '12px' }}>Available Nearby</h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <EquipmentCard
                    image="https://placehold.co/400x300/F5F5F5/4CAF50?text=Tractor"
                    name="Mahindra 575 DI Tractor"
                    owner="Ramesh Kumar"
                    distance="2.5 km"
                    price="₹800/hr"
                    rating="4.8"
                    available="Today"
                    onClick={() => onSelectEquipment({
                        image: "https://placehold.co/400x300/F5F5F5/4CAF50?text=Tractor",
                        name: "Mahindra 575 DI Tractor",
                        owner: "Ramesh Kumar",
                        distance: "2.5 km",
                        price: "₹800/hr",
                        rating: "4.8",
                    })}
                />
                <EquipmentCard
                    image="https://placehold.co/400x300/F5F5F5/FBC02D?text=Harvester"
                    name="Combine Harvester"
                    owner="Suresh Patel"
                    distance="5.0 km"
                    price="₹2,500/acre"
                    rating="4.5"
                    available="Tomorrow"
                    onClick={() => onSelectEquipment({
                        image: "https://placehold.co/400x300/F5F5F5/FBC02D?text=Harvester",
                        name: "Combine Harvester",
                        owner: "Suresh Patel",
                        distance: "5.0 km",
                        price: "₹2,500/acre",
                        rating: "4.5",
                    })}
                />
                <EquipmentCard
                    image="https://placehold.co/400x300/F5F5F5/29B6F6?text=Drone"
                    name="Spraying Drone (10L)"
                    owner="AgriTech Hub"
                    distance="12 km"
                    price="₹400/acre"
                    rating="New"
                    available="Today"
                    onClick={() => onSelectEquipment({
                        image: "https://placehold.co/400x300/F5F5F5/29B6F6?text=Drone",
                        name: "Spraying Drone (10L)",
                        owner: "AgriTech Hub",
                        distance: "12 km",
                        price: "₹400/acre",
                        rating: "New",
                    })}
                />
            </div>
        </div>
    );
};

const EquipmentCard = ({ image, name, owner, distance, price, rating, available, onClick }) => (
    <div className="card" onClick={onClick} style={{ padding: '0', overflow: 'hidden', cursor: 'pointer' }}>
        <div style={{ display: 'flex', height: '120px' }}>
            {/* Image Side */}
            <div style={{ width: '120px', backgroundColor: '#f0f0f0' }}>
                <img src={image} alt={name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            </div>

            {/* Content Side */}
            <div style={{ flex: 1, padding: '12px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                        <h4 style={{ margin: 0, fontSize: '1rem', color: 'var(--color-text-dark)' }}>{name}</h4>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.8rem', fontWeight: 'bold' }}>
                            <Star size={12} fill="#FBC02D" color="#FBC02D" /> {rating}
                        </div>
                    </div>
                    <p style={{ margin: '4px 0 0 0', fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>Owned by {owner}</p>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'end' }}>
                    <div style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>
                        <MapPin size={12} style={{ display: 'inline', marginRight: '4px' }} /> {distance}
                    </div>
                    <div style={{ textAlign: 'right' }}>
                        <div style={{ fontWeight: 'bold', color: 'var(--color-primary-green)', fontSize: '1.1rem' }}>{price}</div>
                    </div>
                </div>
            </div>
        </div>

        {/* Footer Actions */}
        <div style={{
            padding: '12px',
            borderTop: '1px solid var(--color-border)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            backgroundColor: '#FAFAFA'
        }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.9rem', color: '#388E3C', fontWeight: '500' }}>
                <Calendar size={16} /> Available {available}
            </div>
            <button style={{
                padding: '6px 16px',
                backgroundColor: 'var(--color-primary-green)',
                color: 'white',
                borderRadius: '6px',
                fontSize: '0.9rem',
                fontWeight: '600',
                display: 'flex',
                alignItems: 'center',
                gap: '6px'
            }}>
                <PhoneCall size={16} /> Rent Now
            </button>
        </div>
    </div>
);


/* -------------------------------------------------------------------------- */
/* LAND POOLING SECTION                                                       */
/* -------------------------------------------------------------------------- */



export default CollaborativeFarming;
