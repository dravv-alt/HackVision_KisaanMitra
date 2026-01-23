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
import { useLanguage } from '../context/LanguageContext';
import '../styles/layout.css';

const Sidebar = ({ isOpen, onClose }) => {
  const { t } = useLanguage();

  const menuItems = [
    { icon: LayoutDashboard, labelKey: 'dashboard', path: '/dashboard' },
    { icon: Sprout, labelKey: 'farmManagement', path: '/farm-management' },
    { icon: Users, labelKey: 'collaborative', path: '/collaborative' },
    { icon: Package, labelKey: 'inventory', path: '/inventory' },
    { icon: IndianRupee, labelKey: 'financial', path: '/finance' },
    { icon: Landmark, labelKey: 'govSchemes', path: '/schemes' },
    { icon: Bell, labelKey: 'alerts', path: '/alerts' },
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
          <h2 className="app-title">{t('kisanMitra')}</h2>
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
              <span className="nav-label">{t(item.labelKey)}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <p>{t('voiceAssistant')}</p>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
