import React, { createContext, useContext, useState, useEffect } from 'react';
import { t as translate, getCurrentLanguage } from '../utils/translations';

const LanguageContext = createContext();

export const useLanguage = () => {
    const context = useContext(LanguageContext);
    if (!context) {
        throw new Error('useLanguage must be used within LanguageProvider');
    }
    return context;
};

export const LanguageProvider = ({ children }) => {
    const [language, setLanguage] = useState(() => getCurrentLanguage());

    // Listen for language changes in localStorage (from onboarding)
    useEffect(() => {
        const handleStorageChange = () => {
            const newLang = getCurrentLanguage();
            if (newLang !== language) {
                setLanguage(newLang);
            }
        };

        // Check every second for language changes
        const interval = setInterval(handleStorageChange, 1000);

        // Also listen to storage events
        window.addEventListener('storage', handleStorageChange);

        return () => {
            clearInterval(interval);
            window.removeEventListener('storage', handleStorageChange);
        };
    }, [language]);

    const t = (key) => translate(key, language);

    const changeLanguage = (newLanguage) => {
        setLanguage(newLanguage);
        // Update in localStorage
        try {
            const saved = localStorage.getItem('kisanmitra_onboarding');
            if (saved) {
                const data = JSON.parse(saved);
                data.language = newLanguage;
                localStorage.setItem('kisanmitra_onboarding', JSON.stringify(data));
            }
        } catch (e) {
            console.error('Error updating language:', e);
        }
    };

    return (
        <LanguageContext.Provider value={{ language, t, changeLanguage }}>
            {children}
        </LanguageContext.Provider>
    );
};
