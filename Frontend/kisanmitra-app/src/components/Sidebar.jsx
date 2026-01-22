import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Sprout, 
  Users, 
  Package, 
  IndianRupee, 
  Landmark, 
  Bell, 
  X
} from 'lucide-react';
import '../styles/layout.css';

const Sidebar = ({ isOpen, onClose }) => {
  const menuItems = [
    { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
    { icon: Sprout, label: 'Farm Management', path: '/farm-management' },
    { icon: Users, label: 'Collaborative Farming', path: '/collaborative' },
    { icon: Package, label: 'Inventory', path: '/inventory' },
    { icon: IndianRupee, label: 'Financial Tracking', path: '/finance' },
    { icon: Landmark, label: 'Gov Schemes', path: '/schemes' },
    { icon: Bell, label: 'Alerts', path: '/alerts' },
  ];

  return (
    <>
      {/* Overlay for mobile/when open */}
      <div 
        className={`sidebar-overlay ${isOpen ? 'open' : ''}`} 
        onClick={onClose}
      />

      {/* Sidebar Drawer */}
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h2 className="app-title">KisaanMitra</h2>
          <button className="close-btn" onClick={onClose}>
            <X size={24} />
          </button>
        </div>

        <nav className="sidebar-nav">
          {menuItems.map((item) => (
            <NavLink 
              key={item.path} 
              to={item.path}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
              onClick={onClose} // Close on click on mobile
            >
              <item.icon size={24} className="nav-icon" />
              <span className="nav-label">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <p>Voice First Assistant</p>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
