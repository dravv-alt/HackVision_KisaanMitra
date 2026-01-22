import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Sprout, Tractor, Warehouse, ArrowRight, Leaf, Droplets, Activity } from 'lucide-react';
import '../styles/global.css';

const StageCard = ({ title, icon: Icon, description, features, onClick, color }) => (
  <div 
    className="card" 
    onClick={onClick}
    style={{ 
      cursor: 'pointer', 
      transition: 'transform 0.2s',
      borderLeft: `4px solid ${color || 'var(--color-primary-green)'}`,
      height: '100%'
    }}
    onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-4px)'}
    onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
  >
    <div style={{ display: 'flex', alignItems: 'center', marginBottom: '12px' }}>
      <div style={{ 
        backgroundColor: 'var(--color-bg-beige)', 
        padding: '10px', 
        borderRadius: '50%',
        marginRight: '12px'
      }}>
        <Icon size={24} color={color || 'var(--color-primary-green)'} />
      </div>
      <h3 style={{ margin: 0, fontSize: '1.2rem' }}>{title}</h3>
    </div>
    
    <p style={{ color: 'var(--color-text-muted)', marginBottom: '16px', fontSize: '0.9rem' }}>
      {description}
    </p>

    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
      {features.map((feature, idx) => (
        <div key={idx} style={{ display: 'flex', alignItems: 'center', fontSize: '0.85rem', color: 'var(--color-text-dark)' }}>
          <div style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: color, marginRight: '8px' }}></div>
          {feature}
        </div>
      ))}
    </div>

    <div style={{ marginTop: '16px', display: 'flex', alignItems: 'center', color: color || 'var(--color-primary-green)', fontWeight: '600', fontSize: '0.9rem' }}>
      Open Stage <ArrowRight size={16} style={{ marginLeft: '4px' }} />
    </div>
  </div>
);

const FarmManagement = () => {
  const navigate = useNavigate();

  return (
    <div style={{ paddingBottom: '80px' }}>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.5rem', marginBottom: '8px' }}>Farm Management</h2>
        <p style={{ color: 'var(--color-text-muted)' }}>Manage your crop lifecycle from planning to harvest.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '16px' }}>
        <StageCard
          title="Planning Stage"
          icon={Sprout}
          color="#4CAF50" // Primary Green
          description="Choose the best crop for your soil and season to maximize profit."
          features={['Crop Selection Recommender', 'Government Schemes']}
          onClick={() => navigate('/farm-management/planning')}
        />

        <StageCard
          title="Farming Stage"
          icon={Tractor}
          color="#F9A825" // Dark Yellow/Gold
          description="Monitor crop health and optimize inputs effectively."
          features={['Crop Doctor (Disease Detection)', 'Smart Irrigation', 'Fertilizer Optimization']}
          onClick={() => navigate('/farm-management/farming')}
        />

        <StageCard
          title="Post-Harvest Stage"
          icon={Warehouse}
          color="#795548" // Brown
          description="Decide when to sell and how to manage crop residue."
          features={['Market Price Prediction', 'Residual Management (Bio-fuel)']}
          onClick={() => navigate('/farm-management/post-harvest')}
        />
      </div>
    </div>
  );
};

export default FarmManagement;
