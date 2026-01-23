import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

/**
 * Component to protect onboarding routes
 * Redirects to dashboard if onboarding is already completed
 */
const OnboardingGuard = ({ children }) => {
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const isCompleted = localStorage.getItem('kisanmitra_onboarding_completed') === 'true';

        // If onboarding is completed and user tries to access onboarding routes
        if (isCompleted && location.pathname.startsWith('/onboarding')) {
            navigate('/dashboard', { replace: true });
        }
    }, [location.pathname, navigate]);

    return children;
};

export default OnboardingGuard;
