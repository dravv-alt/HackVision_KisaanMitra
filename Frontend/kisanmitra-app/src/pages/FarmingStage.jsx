import React, { useState } from 'react';
import { ArrowLeft, Camera, Droplets, Zap, AlertTriangle, Upload, CheckCircle, CloudRain } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import '../styles/global.css';

const FarmingStage = () => {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('doctor'); // doctor | irrigation | inputs

    return (
        <div style={{ paddingBottom: '80px' }}>
            {/* Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
                <button
                    onClick={() => navigate('/farm-management')}
                    style={{ background: 'none', padding: '4px' }}
                >
                    <ArrowLeft size={24} color="var(--color-text-dark)" />
                </button>
                <h2 style={{ fontSize: '1.25rem', margin: 0 }}>Farming Stage</h2>
            </div>

            {/* Tabs */}
            <div style={{
                display: 'flex',
                gap: '12px',
                overflowX: 'auto',
                paddingBottom: '4px',
                marginBottom: '24px'
            }}>
                {[
                    { id: 'doctor', label: 'Crop Doctor', icon: Camera },
                    { id: 'irrigation', label: 'Smart Irrigation', icon: Droplets },
                    { id: 'inputs', label: 'Input Optimizer', icon: Zap },
                ].map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        style={{
                            flex: '0 0 auto',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px',
                            padding: '10px 16px',
                            borderRadius: '24px',
                            border: activeTab === tab.id ? 'none' : '1px solid var(--color-border)',
                            backgroundColor: activeTab === tab.id ? 'var(--color-primary-green)' : 'white',
                            color: activeTab === tab.id ? 'white' : 'var(--color-text-dark)',
                            fontWeight: '500',
                            fontSize: '0.9rem'
                        }}
                    >
                        <tab.icon size={18} />
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Content Area */}
            {activeTab === 'doctor' && <CropDoctorSection />}
            {activeTab === 'irrigation' && <IrrigationSection />}
            {activeTab === 'inputs' && <InputOptimizerSection />}
        </div>
    );
};

// 1. Crop Doctor Component
const CropDoctorSection = () => {
    const [image, setImage] = useState(null);
    const [analyzing, setAnalyzing] = useState(false);
    const [result, setResult] = useState(null);

    const handleUpload = (e) => {
        // Mock upload
        const file = e.target.files[0];
        if (file) {
            setImage(URL.createObjectURL(file));
            setAnalyzing(true);
            // Simulate API call
            setTimeout(() => {
                setAnalyzing(false);
                setResult({
                    disease: 'Yellow Rust',
                    severity: 'Warning',
                    cause: 'Fungal infection due to high humidity.',
                    remedy: 'Spray Propiconazole 25 EC @ 1ml/liter of water.',
                    dosage: '200ml per acre'
                });
            }, 2000);
        }
    };

    return (
        <div className="card">
            <h3 style={{ marginBottom: '16px' }}>Crop Diagnosis</h3>

            {!image ? (
                <label style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    border: '2px dashed var(--color-border)',
                    borderRadius: '12px',
                    padding: '40px 20px',
                    cursor: 'pointer',
                    backgroundColor: '#FAFAFA'
                }}>
                    <Camera size={48} color="#9E9E9E" style={{ marginBottom: '12px' }} />
                    <span style={{ fontWeight: '500', color: 'var(--color-text-dark)' }}>Take a Photo or Upload</span>
                    <span style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>of the affected leaf</span>
                    <input type="file" accept="image/*" hidden onChange={handleUpload} />
                </label>
            ) : (
                <div>
                    <img src={image} alt="Crop" style={{ width: '100%', height: '200px', objectFit: 'cover', borderRadius: '12px', marginBottom: '16px' }} />

                    {analyzing ? (
                        <div style={{ textAlign: 'center', padding: '20px' }}>
                            <div className="spinner" style={{ marginBottom: '8px' }}>⏳</div>
                            <p>Analyzing crop health...</p>
                        </div>
                    ) : result ? (
                        <div style={{ animation: 'fadeIn 0.5s' }}>
                            <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px',
                                padding: '12px',
                                backgroundColor: '#FFF3E0',
                                borderRadius: '8px',
                                color: '#EF6C00',
                                marginBottom: '16px'
                            }}>
                                <AlertTriangle size={20} />
                                <span style={{ fontWeight: 'bold' }}>{result.disease} Detected</span>
                            </div>

                            <div style={{ marginBottom: '16px' }}>
                                <h4 style={{ fontSize: '0.95rem', marginBottom: '4px' }}>Cause</h4>
                                <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>{result.cause}</p>
                            </div>

                            <div style={{ marginBottom: '16px' }}>
                                <h4 style={{ fontSize: '0.95rem', marginBottom: '4px' }}>Recommended Treatment</h4>
                                <p style={{ fontSize: '0.9rem', color: 'var(--color-text-dark)' }}>{result.remedy}</p>
                            </div>

                            <div style={{ padding: '12px', backgroundColor: '#E8F5E9', borderRadius: '8px', display: 'flex', justifyContent: 'space-between' }}>
                                <span style={{ fontSize: '0.9rem' }}>Dosage:</span>
                                <span style={{ fontWeight: 'bold', color: '#2E7D32' }}>{result.dosage}</span>
                            </div>

                            <button onClick={() => { setImage(null); setResult(null); }} style={{ marginTop: '16px', width: '100%', padding: '12px', border: '1px solid var(--color-border)', borderRadius: '8px', background: 'white' }}>
                                Analyze Another
                            </button>
                        </div>
                    ) : null}
                </div>
            )}
        </div>
    );
};

// 2. Smart Irrigation Component
const IrrigationSection = () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div className="card" style={{ background: 'linear-gradient(to right, #E3F2FD, #FFFFFF)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                <Droplets size={24} color="#0288D1" />
                <h3 style={{ margin: 0 }}>Watering Advice</h3>
            </div>

            <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#0288D1', marginBottom: '8px' }}>
                Do Not Water Today
            </div>
            <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)' }}>
                Soil moisture is adequate (45%). Rain expected tomorrow (80% chance).
            </p>
        </div>

        <div className="card">
            <h4 style={{ marginBottom: '12px' }}>Schedule</h4>
            {[
                { day: 'Today', status: 'Skip', icon: <CheckCircle size={16} color="green" /> },
                { day: 'Tomorrow', status: 'Rain Expected', icon: <CloudRain size={16} color="blue" /> },
                { day: 'Wed', status: 'Water (Morning)', icon: <Droplets size={16} color="orange" /> },
            ].map((item, i) => (
                <div key={i} style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    padding: '12px 0',
                    borderBottom: i !== 2 ? '1px solid var(--color-border)' : 'none'
                }}>
                    <span>{item.day}</span>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem' }}>
                        {item.status} {item.icon}
                    </div>
                </div>
            ))}
        </div>
    </div>
);

// 3. Input Optimizer Component
const InputOptimizerSection = () => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div className="card">
            <h3 style={{ marginBottom: '16px' }}>Recommended Inputs</h3>
            <p style={{ fontSize: '0.9rem', color: 'var(--color-text-muted)', marginBottom: '16px' }}>
                Based on your crop stage (Flowering)
            </p>

            <InputCard
                type="Fertilizer"
                name="Urea (Neem Coated)"
                qty="40 kg/acre"
                timing="Apply within 2 days"
                cost="₹266"
            />
            <InputCard
                type="Pesticide"
                name="Imidacloprid"
                qty="100 ml/acre"
                timing="Preventative (Optional)"
                cost="₹350"
            />
        </div>
    </div>
);

const InputCard = ({ type, name, qty, timing, cost }) => (
    <div style={{
        border: '1px solid var(--color-border)',
        borderRadius: '12px',
        padding: '12px',
        marginBottom: '12px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
    }}>
        <div>
            <div style={{ fontSize: '0.8rem', color: type === 'Fertilizer' ? '#F57F17' : '#D32F2F', fontWeight: 'bold', marginBottom: '2px' }}>
                {type.toUpperCase()}
            </div>
            <div style={{ fontWeight: '600', marginBottom: '4px' }}>{name}</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>{qty} • {timing}</div>
        </div>
        <div style={{ textAlign: 'right' }}>
            <div style={{ fontWeight: 'bold' }}>{cost}</div>
            <button style={{
                marginTop: '4px',
                padding: '4px 8px',
                fontSize: '0.8rem',
                backgroundColor: 'var(--color-bg-beige)',
                color: 'var(--color-text-dark)',
                borderRadius: '4px'
            }}>
                Add
            </button>
        </div>
    </div>
);

export default FarmingStage;
