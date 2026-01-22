import React, { useState } from 'react';
import { Menu } from 'lucide-react';
import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import VoiceAgent from './VoiceAgent';
import '../styles/layout.css';

const Layout = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const location = useLocation();

    const getPageTitle = (pathname) => {
        switch (pathname) {
            case '/': return 'Dashboard';
            case '/farm-management': return 'Farm Management';
            case '/collaborative': return 'Collaborative Farming';
            case '/inventory': return 'Inventory';
            case '/finance': return 'Financial Tracking';
            case '/schemes': return 'Government Schemes';
            case '/alerts': return 'Alerts';
            default: return 'KisaanMitra';
        }
    };

    return (
        <div className="app-container">
            <header className="main-header">
                <button
                    className="menu-btn"
                    onClick={() => setIsSidebarOpen(true)}
                    aria-label="Open Menu"
                >
                    <Menu size={28} />
                </button>
                <h1 className="header-title">{getPageTitle(location.pathname)}</h1>
            </header>

            <Sidebar
                isOpen={isSidebarOpen}
                onClose={() => setIsSidebarOpen(false)}
            />

            <main className="main-content">
                <Outlet />
            </main>

            <VoiceAgent />
        </div>
    );
};

export default Layout;
