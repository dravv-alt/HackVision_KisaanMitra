import React, { useState } from 'react';
import { ArrowLeft, Check, Sprout, TrendingUp, ShieldCheck, CloudRain } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import MapComponent from '../components/MapComponent';
import '../styles/global.css';

const CropCard = ({ crop, recommended }) => (
    <div className="card" style={{
        marginBottom: '16px',
        border: recommended ? '2px solid var(--color-primary-green)' : '1px solid transparent',
        position: 'relative'
    }}>
        {recommended && (
            <div style={{
                position: 'absolute',
                top: '-12px',
                right: '16px',
                backgroundColor: 'var(--color-primary-green)',
                color: 'white',
                padding: '4px 12px',
                borderRadius: '12px',
                fontSize: '0.8rem',
                fontWeight: 'bold'
            }}>
                Best Choice
            </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '12px' }}>
            <div>
                <h3 style={{ fontSize: '1.25rem', marginBottom: '4px' }}>{crop.name}</h3>
                <p style={{ color: 'var(--color-text-muted)', fontSize: '0.9rem' }}>{crop.duration} days • {crop.season}</p>
            </div>
            <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: 'var(--color-text-dark)' }}>{crop.profit}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>Exp. Profit/Acre</div>
            </div>
        </div>

        <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '16px' }}>
            <span style={{
                padding: '4px 8px', borderRadius: '4px', fontSize: '0.8rem',
                backgroundColor: '#E8F5E9', color: '#2E7D32', display: 'flex', alignItems: 'center', gap: '4px'
            }}>
                <TrendingUp size={14} /> High Demand
            </span>
            <span style={{
                padding: '4px 8px', borderRadius: '4px', fontSize: '0.8rem',
                backgroundColor: '#FFF3E0', color: '#EF6C00', display: 'flex', alignItems: 'center', gap: '4px'
            }}>
                <ShieldCheck size={14} /> Low Risk
            </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', fontSize: '0.9rem', color: 'var(--color-text-muted)', marginBottom: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <CloudRain size={16} /> Suitable Weather
            </div>
            <div>Soil: {crop.soil}</div>
        </div>

        <button style={{
            width: '100%',
            padding: '12px',
            backgroundColor: 'var(--color-primary-green)',
            color: 'white',
            borderRadius: '8px',
            fontWeight: '600',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px'
        }}>
            Select {crop.name} <Check size={18} />
        </button>
    </div>
);

const PlanningStage = () => {
    const navigate = useNavigate();
    const [step, setStep] = useState(1); // 1: Input Details, 2: Recommendations

    // Mock Request Data
    const [formData, setFormData] = useState({
        area: '',
        unit: 'acre',
        soil: 'Black Soil',
        season: 'Rabi'
    });

    const handleNext = () => {
        // In real app, call API here
        setStep(2);
    };

    return (
        <div style={{ paddingBottom: '80px' }}>
            {/* Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
                <button
                    onClick={() => step === 1 ? navigate('/farm-management') : setStep(1)}
                    style={{ background: 'none', padding: '4px' }}
                >
                    <ArrowLeft size={24} color="var(--color-text-dark)" />
                </button>
                <h2 style={{ fontSize: '1.25rem', margin: 0 }}>
                    {step === 1 ? 'Planning: Farm Details' : 'Recommended Crops'}
                </h2>
            </div>

            {step === 1 ? (
                <div style={{ maxWidth: '600px', margin: '0 auto' }}>
                    <div className="card">
                        <h3 style={{ marginBottom: '16px', fontSize: '1.1rem' }}>Enter Details</h3>

                        <div style={{ marginBottom: '16px' }}>
                            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Farm Size</label>
                            <div style={{ display: 'flex', gap: '8px' }}>
                                <input
                                    type="number"
                                    placeholder="e.g. 5"
                                    value={formData.area}
                                    onChange={(e) => setFormData({ ...formData, area: e.target.value })}
                                    style={{
                                        flex: 1,
                                        padding: '12px',
                                        borderRadius: '8px',
                                        border: '1px solid #ccc',
                                        fontSize: '1rem'
                                    }}
                                />
                                <select
                                    value={formData.unit}
                                    onChange={(e) => setFormData({ ...formData, unit: e.target.value })}
                                    style={{
                                        padding: '12px',
                                        borderRadius: '8px',
                                        border: '1px solid #ccc',
                                        backgroundColor: 'white',
                                        fontSize: '1rem'
                                    }}
                                >
                                    <option value="acre">Acre</option>
                                    <option value="bigha">Bigha</option>
                                    <option value="hectare">Hectare</option>
                                </select>
                            </div>
                        </div>

                        <div style={{ marginBottom: '16px' }}>
                            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Soil Type</label>
                            <select
                                value={formData.soil}
                                onChange={(e) => setFormData({ ...formData, soil: e.target.value })}
                                style={{
                                    width: '100%',
                                    padding: '12px',
                                    borderRadius: '8px',
                                    border: '1px solid #ccc',
                                    backgroundColor: 'white',
                                    fontSize: '1rem'
                                }}
                            >
                                <option value="Black Soil">Black Soil (Kali Mitti)</option>
                                <option value="Red Soil">Red Soil (Lal Mitti)</option>
                                <option value="Alluvial Soil">Alluvial Soil (Jalodh Mitti)</option>
                            </select>
                        </div>

                        <div style={{ marginBottom: '24px' }}>
                            <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>Season</label>
                            <select
                                value={formData.season}
                                onChange={(e) => setFormData({ ...formData, season: e.target.value })}
                                style={{
                                    width: '100%',
                                    padding: '12px',
                                    borderRadius: '8px',
                                    border: '1px solid #ccc',
                                    backgroundColor: 'white',
                                    fontSize: '1rem'
                                }}
                            >
                                <option value="Rabi">Rabi (Winter)</option>
                                <option value="Kharif">Kharif (Monsoon)</option>
                                <option value="Zaid">Zaid (Summer)</option>
                            </select>
                        </div>

                        <button
                            onClick={handleNext}
                            style={{
                                width: '100%',
                                padding: '14px',
                                backgroundColor: 'var(--color-primary-green)',
                                color: 'white',
                                borderRadius: '8px',
                                fontWeight: 'bold',
                                fontSize: '1rem'
                            }}
                        >
                            Find Best Crops
                        </button>
                    </div>
                </div>
            ) : (
                <div style={{ maxWidth: '600px', margin: '0 auto' }}>
                    <div className="card" style={{ padding: '0', overflow: 'hidden', marginBottom: '24px', border: '1px solid var(--color-border)' }}>
                        <MapComponent
                            lat={30.90}
                            lon={75.85}
                            height="180px"
                            zoom={13}
                            markers={[
                                { lat: 30.90, lon: 75.85, popupText: "Your Farm Location" }
                            ]}
                        />
                        <div style={{ padding: '8px 16px', background: '#F1F8E9', color: '#33691E', fontSize: '0.9rem', fontWeight: '500' }}>
                            Soil Analysis for: {formData.area} {formData.unit} in Ludhiana
                        </div>
                    </div>

                    <p style={{ marginBottom: '16px', color: 'var(--color-text-muted)' }}>
                        Based on <strong>{formData.area} {formData.unit}</strong> of <strong>{formData.soil}</strong> in <strong>{formData.season}</strong> season.
                    </p>

                    <CropCard
                        recommended={true}
                        crop={{
                            name: 'Wheat (Sharbati)',
                            duration: 120,
                            season: 'Rabi',
                            profit: '₹25,000',
                            soil: 'Target Match'
                        }}
                    />

                    <CropCard
                        recommended={false}
                        crop={{
                            name: 'Mustard',
                            duration: 100,
                            season: 'Rabi',
                            profit: '₹18,000',
                            soil: 'Compatible'
                        }}
                    />

                    <CropCard
                        recommended={false}
                        crop={{
                            name: 'Chickpea (Chana)',
                            duration: 110,
                            season: 'Rabi',
                            profit: '₹20,000',
                            soil: 'Compatible'
                        }}
                    />
                </div>
            )}
        </div>
    );
};

export default PlanningStage;
