import React, { useState } from 'react';
import {
    ArrowLeft,
    Star,
    MapPin,
    Truck,
    Calendar,
    Check,
    Mic
} from 'lucide-react';
import '../styles/global.css';
import MapComponent from './MapComponent';

const EquipmentRentalDetails = ({ equipment, onBack, onConfirm }) => {
    // Mock data/state for selected dates
    const [selectedDates, setSelectedDates] = useState({
        start: 'Oct 24',
        end: 'Oct 26',
        days: 3
    });

    const dailyRate = 800;
    const totalCost = dailyRate * selectedDates.days;

    return (
        <div style={{ paddingBottom: '80px' }}>
            {/* Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
                <button
                    onClick={onBack}
                    style={{
                        background: 'none',
                        padding: '8px',
                        borderRadius: '50%',
                        color: 'var(--color-text-dark)',
                        border: '1px solid var(--color-border)'
                    }}
                >
                    <ArrowLeft size={24} />
                </button>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 'bold', margin: 0 }}>Equipment Details</h2>
            </div>

            {/* Main Content Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px' }}>

                {/* Left Column: Images & Info */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>

                    {/* Hero Image Card */}
                    <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
                        <div style={{
                            height: '300px',
                            backgroundColor: '#E0DBC8',
                            position: 'relative',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}>
                            {equipment.image ? (
                                <img src={equipment.image} alt={equipment.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                            ) : (
                                // Fallback icon if no image
                                <div style={{ textAlign: 'center', color: 'rgba(76, 175, 80, 0.4)' }}>
                                    <span style={{ fontSize: '5rem' }}>🚜</span>
                                </div>
                            )}

                            <div style={{
                                position: 'absolute',
                                bottom: '16px',
                                left: '16px',
                                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                                padding: '8px 12px',
                                borderRadius: '8px',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '6px',
                                fontSize: '0.85rem',
                                fontWeight: 'bold',
                                boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                            }}>
                                <Check size={16} color="var(--color-accent-ochre)" strokeWidth={3} />
                                Verified Equipment
                            </div>
                        </div>

                        <div style={{ padding: '24px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
                                <div>
                                    <h2 style={{ fontSize: '1.5rem', fontWeight: '800', margin: '0 0 4px 0' }}>{equipment.name || 'Rotavator (7 Feet)'}</h2>
                                    <p style={{ color: 'var(--color-text-muted)', fontSize: '1rem' }}>Mahindra Heavy Duty Series • 2022 Model</p>
                                </div>
                                <div style={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '4px',
                                    padding: '6px 12px',
                                    borderRadius: '20px',
                                    border: '1px solid var(--color-border)',
                                    backgroundColor: 'white'
                                }}>
                                    <Star size={16} fill="var(--color-accent-ochre)" color="var(--color-accent-ochre)" />
                                    <span style={{ fontWeight: 'bold' }}>{equipment.rating || '4.8'}</span>
                                    <span style={{ color: 'var(--color-text-muted)', fontSize: '0.85rem' }}>(24)</span>
                                </div>
                            </div>

                            <div style={{ height: '1px', backgroundColor: 'var(--color-border)', margin: '0 0 24px 0' }}></div>

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '24px' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                    <div style={{
                                        width: '48px',
                                        height: '48px',
                                        borderRadius: '50%',
                                        overflow: 'hidden',
                                        backgroundColor: '#eee',
                                        border: '2px solid white',
                                        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                                    }}>
                                        <img src="https://placehold.co/100x100?text=RK" alt="Owner" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                                    </div>
                                    <div>
                                        <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', margin: 0 }}>Owned by</p>
                                        <p style={{ fontWeight: 'bold', margin: 0 }}>{equipment.owner || 'Ramesh Kumar'}</p>
                                    </div>
                                </div>
                                <div style={{ display: 'flex', gap: '24px' }}>
                                    <div>
                                        <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', margin: 0 }}>Condition</p>
                                        <p style={{ fontWeight: 'bold', margin: 0 }}>Excellent</p>
                                    </div>
                                    <div>
                                        <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', margin: 0 }}>HP Required</p>
                                        <p style={{ fontWeight: 'bold', margin: 0 }}>45-50 HP</p>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <h3 style={{ fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '8px' }}>About this equipment</h3>
                                <p style={{ color: 'var(--color-text-muted)', lineHeight: '1.6' }}>
                                    Heavy-duty rotavator suitable for all soil types. Well maintained and regularly serviced. It ensures fine seedbed preparation for your Kharif and Rabi crops. Available for immediate booking in Ludhiana district.
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* Location & Proximity */}
                    <div className="card">
                        <h3 style={{ fontSize: '1.1rem', fontWeight: 'bold', marginBottom: '16px' }}>Location & Proximity</h3>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                            {/* Map Placeholder - REPLACED WITH REAL MAP */}
                            <div style={{
                                height: '160px',
                                borderRadius: '12px',
                                overflow: 'hidden',
                                border: '1px solid var(--color-border)',
                                marginBottom: '0'
                            }}>
                                <MapComponent
                                    lat={30.91}
                                    lon={75.85}
                                    height="100%"
                                    zoom={14}
                                    markers={[{ lat: 30.91, lon: 75.85, popupText: equipment.name }]}
                                />
                            </div>

                            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                                <div style={{ display: 'flex', gap: '12px', alignItems: 'start' }}>
                                    <div style={{ padding: '8px', backgroundColor: 'white', borderRadius: '8px', border: '1px solid var(--color-border)' }}>
                                        <MapPin size={20} color="var(--color-primary-green)" />
                                    </div>
                                    <div>
                                        <p style={{ fontWeight: 'bold', margin: 0 }}>{equipment.distance || '2.5 km'} away</p>
                                        <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', margin: 0 }}>Village Raipur, Near Main Canal</p>
                                    </div>
                                </div>

                                <div style={{ display: 'flex', gap: '12px', alignItems: 'start' }}>
                                    <div style={{ padding: '8px', backgroundColor: 'white', borderRadius: '8px', border: '1px solid var(--color-border)' }}>
                                        <Truck size={20} color="var(--color-text-muted)" />
                                    </div>
                                    <div>
                                        <p style={{ fontWeight: 'bold', margin: 0 }}>Self Pickup</p>
                                        <p style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)', margin: 0 }}>Transport not included</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                </div>

                {/* Right Column: Booking Action */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                    <div className="card" style={{ position: 'sticky', top: '24px', backgroundColor: 'white', border: '1px solid var(--color-border)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'end', marginBottom: '24px' }}>
                            <div>
                                <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', fontWeight: '500' }}>Daily Rate</p>
                                <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px' }}>
                                    <span style={{ fontSize: '1.8rem', fontWeight: 'bold' }}>₹{equipment.price ? parseInt(equipment.price.replace(/[^\d]/g, '')) : dailyRate}</span>
                                    <span style={{ color: 'var(--color-text-muted)' }}>/ day</span>
                                </div>
                            </div>
                            <div style={{
                                padding: '4px 12px',
                                backgroundColor: '#E8F5E9',
                                color: 'var(--color-primary-green)',
                                borderRadius: '16px',
                                fontSize: '0.75rem',
                                fontWeight: 'bold',
                                border: '1px solid #C8E6C9'
                            }}>
                                Available Now
                            </div>
                        </div>

                        <div style={{ marginBottom: '24px' }}>
                            <label style={{ display: 'block', fontSize: '0.9rem', fontWeight: 'bold', marginBottom: '8px' }}>Selected Dates</label>
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'space-between',
                                padding: '12px',
                                backgroundColor: 'var(--color-bg-beige)',
                                borderRadius: '12px',
                                border: '1px solid var(--color-border)',
                                cursor: 'pointer'
                            }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                    <Calendar size={20} color="var(--color-primary-green)" />
                                    <span style={{ fontWeight: '500' }}>{selectedDates.start} - {selectedDates.end}</span>
                                </div>
                                <span style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>{selectedDates.days} Days</span>
                            </div>
                        </div>

                        <div style={{ padding: '16px', backgroundColor: 'var(--color-bg-beige)', borderRadius: '12px', marginBottom: '24px' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '8px', color: 'var(--color-text-muted)' }}>
                                <span>₹{dailyRate} x {selectedDates.days} days</span>
                                <span style={{ fontWeight: '500', color: 'var(--color-text-dark)' }}>₹{totalCost}</span>
                            </div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', marginBottom: '12px', color: 'var(--color-text-muted)' }}>
                                <span>Service Fee</span>
                                <span style={{ fontWeight: '500', color: 'var(--color-primary-green)' }}>Free</span>
                            </div>
                            <div style={{ height: '1px', backgroundColor: 'var(--color-border)', marginBottom: '12px' }}></div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '1.1rem', fontWeight: 'bold' }}>
                                <span>Total</span>
                                <span>₹{totalCost}</span>
                            </div>
                        </div>

                        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                            <button
                                onClick={() => onConfirm({ ...equipment, totalCost, days: selectedDates.days })}
                                style={{
                                    width: '100%',
                                    padding: '14px',
                                    backgroundColor: 'var(--color-primary-green)',
                                    color: 'white',
                                    fontSize: '1.1rem',
                                    fontWeight: 'bold',
                                    borderRadius: '12px',
                                    boxShadow: '0 4px 12px rgba(76, 175, 80, 0.2)',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    gap: '8px'
                                }}>
                                Confirm Booking
                            </button>

                            <button style={{
                                width: '100%',
                                padding: '14px',
                                backgroundColor: 'transparent',
                                color: 'var(--color-primary-green)',
                                border: '2px solid var(--color-primary-green)',
                                fontSize: '1.1rem',
                                fontWeight: 'bold',
                                borderRadius: '12px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                gap: '8px'
                            }}>
                                <Mic size={20} /> Request via Voice
                            </button>
                        </div>

                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px', marginTop: '16px', fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>
                            <span style={{ fontSize: '1.2rem' }}>🛡️</span> Secure payment & Verified Owner
                        </div>

                    </div>
                </div>

            </div>
        </div>
    );
};

export default EquipmentRentalDetails;
