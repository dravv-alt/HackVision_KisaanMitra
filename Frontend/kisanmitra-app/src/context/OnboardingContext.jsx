import React, { createContext, useContext, useState, useEffect } from 'react';
import { t } from '../utils/translations';

const OnboardingContext = createContext();

export const useOnboarding = () => {
    const context = useContext(OnboardingContext);
    if (!context) {
        throw new Error('useOnboarding must be used within OnboardingProvider');
    }
    return context;
};

export const OnboardingProvider = ({ children }) => {
    const [onboardingData, setOnboardingData] = useState(() => {
        // Load from localStorage if available
        const saved = localStorage.getItem('kisanmitra_onboarding');
        return saved ? JSON.parse(saved) : {
            language: '',
            location: {
                state: '',
                district: '',
                village: '',
                pincode: '',
                lat: null,
                lon: null
            },
            soilType: '',
            farmSize: '',
            farmSizeUnit: 'Bigha',
            selectedCrops: [],
            userId: null,
            farmerId: null
        };
    });

    // Save to localStorage whenever data changes
    useEffect(() => {
        localStorage.setItem('kisanmitra_onboarding', JSON.stringify(onboardingData));
    }, [onboardingData]);

    const updateOnboardingData = (field, value) => {
        setOnboardingData(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const updateLocation = (locationData) => {
        setOnboardingData(prev => ({
            ...prev,
            location: {
                ...prev.location,
                ...locationData
            }
        }));
    };

    const clearOnboardingData = () => {
        setOnboardingData({
            language: '',
            location: {
                state: '',
                district: '',
                village: '',
                pincode: '',
                lat: null,
                lon: null
            },
            soilType: '',
            farmSize: '',
            farmSizeUnit: 'Bigha',
            selectedCrops: [],
            userId: null,
            farmerId: null
        });
        localStorage.removeItem('kisanmitra_onboarding');
    };

    const saveFarmerProfile = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/v1/onboarding/complete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    language: onboardingData.language,
                    location: onboardingData.location,
                    soilType: onboardingData.soilType,
                    landSizeAcres: convertToAcres(onboardingData.farmSize, onboardingData.farmSizeUnit),
                    selectedCrops: onboardingData.selectedCrops
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to save farmer profile');
            }

            const data = await response.json();

            // Update with farmer ID from backend
            setOnboardingData(prev => ({
                ...prev,
                userId: data.userId,
                farmerId: data.farmerId
            }));

            return data;
        } catch (error) {
            console.error('Error saving farmer profile:', error);
            throw error;
        }
    };

    const convertToAcres = (size, unit) => {
        const sizeNum = parseFloat(size) || 0;
        if (unit === 'Acre') return sizeNum;
        if (unit === 'Bigha') return sizeNum * 0.625; // 1 Bigha ≈ 0.625 Acres
        return sizeNum;
    };

    return (
        <OnboardingContext.Provider value={{
            onboardingData,
            updateOnboardingData,
            updateLocation,
            clearOnboardingData,
            saveFarmerProfile,
            t: (key) => t(key, onboardingData.language || 'en')
        }}>
            {children}
        </OnboardingContext.Provider>
    );
};
