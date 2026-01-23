import React, { useState } from 'react';
import { Menu } from 'lucide-react';
import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import VoiceAgent from './VoiceAgent';
import { useLanguage } from '../context/LanguageContext';
import '../styles/layout.css';

const Layout = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const location = useLocation();
    const { t } = useLanguage();

    const getPageTitle = (pathname) => {
        switch (pathname) {
            case '/dashboard': return t('dashboard');
            case '/farm-management': return t('farmManagement');
            case '/farm-management/planning': return t('planningStage');
            case '/farm-management/farming': return t('farmingStage');
            case '/farm-management/post-harvest': return t('postHarvest');
            case '/farm-management/calendar': return t('farmingCalendar');
            case '/collaborative': return t('collaborative');
            case '/inventory': return t('inventory');
            case '/finance': return t('finance');
            case '/schemes': return t('govSchemes');
            case '/alerts': return t('priorityAlerts');
            case '/active-crops': return t('activeCrops');
            default: return t('kisanMitra');
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
