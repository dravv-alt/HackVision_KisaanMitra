import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useOnboarding } from '../../context/OnboardingContext';

const LanguageSelection = () => {
    const navigate = useNavigate();
    const { onboardingData, updateOnboardingData } = useOnboarding();
    const [selected, setSelected] = useState(onboardingData.language || 'hi');
    // Snippet shows Hindi checked, Marathi unchecked.

    // Helper to get classes for selected vs unselected
    const getCardClasses = (lang) => {
        const isSelected = selected === lang;
        if (isSelected) {
            return "relative group flex flex-col md:flex-row items-center justify-between md:justify-center gap-3 rounded-xl border-2 border-[#9CAF88] bg-[#E8EFE6] p-5 shadow-sm transition-all hover:shadow-md cursor-pointer";
        }
        return "relative group flex flex-col md:flex-row items-center justify-between md:justify-center gap-3 rounded-xl border border-[#E6DCC8] bg-[#FFF8E1] p-5 shadow-sm transition-all hover:border-[#9CAF88]/50 cursor-pointer";
    }

    return (
        <div className="bg-[#F5F2EA] text-[#2C3E2C] font-['Plus_Jakarta_Sans'] overflow-x-hidden min-h-screen flex flex-col">
            <header className="w-full flex justify-center bg-[#F5F2EA] border-b border-[#E6DCC8] px-4 py-4">
                <div className="w-full max-w-[960px] flex items-center justify-between">
                    <div className="flex items-center gap-3 text-[#2C3E2C]">
                        <div className="size-8 flex items-center justify-center text-[#9CAF88]">
                            <span className="material-symbols-outlined text-3xl">agriculture</span>
                        </div>
                        <h2 className="text-[#2C3E2C] text-xl font-bold leading-tight tracking-[-0.015em]">KisanMitra</h2>
                    </div>
                    <button aria-disabled="true" className="flex items-center justify-center size-10 rounded-lg bg-transparent text-[#2C3E2C]/40 cursor-not-allowed">
                        <span className="material-symbols-outlined text-3xl">menu</span>
                    </button>
                </div>
            </header>
            <div className="flex-1 flex flex-col items-center justify-center px-4 py-8 md:py-12">
                <div className="w-full max-w-[500px] flex flex-col gap-8">
                    <div className="flex flex-col gap-2 text-center md:text-left">
                        <h1 className="text-[#2C3E2C] text-4xl md:text-5xl font-black leading-tight tracking-[-0.02em]">Apni Bhasha Chune</h1>
                        <p className="text-[#9CAF88] font-bold text-lg leading-normal">Choose your language</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

                        {/* Hindi */}
                        <div onClick={() => setSelected('hi')} className={getCardClasses('hi')}>
                            <div className="flex items-center gap-3">
                                <div className="flex flex-col items-start md:items-center">
                                    <span className="text-[#2C3E2C] text-xl font-bold leading-tight">हिंदी</span>
                                    <span className="text-[#9CAF88] text-sm font-bold">Hindi</span>
                                </div>
                            </div>
                            <div className={`absolute top-3 right-3 md:static md:top-auto md:right-auto ${selected === 'hi' ? 'text-[#9CAF88]' : 'text-[#D1C6B4]'}`}>
                                <span className="material-symbols-outlined text-2xl">{selected === 'hi' ? 'check_circle' : 'radio_button_unchecked'}</span>
                            </div>
                        </div>

                        {/* Marathi */}
                        <div onClick={() => setSelected('mr')} className={getCardClasses('mr')}>
                            <div className="flex items-center gap-3">
                                <div className="flex flex-col items-start md:items-center">
                                    <span className="text-[#2C3E2C] text-xl font-bold leading-tight">मराठी</span>
                                    <span className="text-neutral-500 text-sm font-medium">Marathi</span>
                                </div>
                            </div>
                            <div className={`absolute top-3 right-3 md:static md:top-auto md:right-auto ${selected === 'mr' ? 'text-[#9CAF88]' : 'text-[#D1C6B4]'}`}>
                                <span className="material-symbols-outlined text-2xl">{selected === 'mr' ? 'check_circle' : 'radio_button_unchecked'}</span>
                            </div>
                        </div>

                        {/* English */}
                        <div onClick={() => setSelected('en')} className={getCardClasses('en')}>
                            <div className="flex items-center gap-3">
                                <div className="flex flex-col items-start md:items-center">
                                    <span className="text-[#2C3E2C] text-xl font-bold leading-tight">English</span>
                                    <span className="text-neutral-500 text-sm font-medium">English</span>
                                </div>
                            </div>
                            <div className={`absolute top-3 right-3 md:static md:top-auto md:right-auto ${selected === 'en' ? 'text-[#9CAF88]' : 'text-[#D1C6B4]'}`}>
                                <span className="material-symbols-outlined text-2xl">{selected === 'en' ? 'check_circle' : 'radio_button_unchecked'}</span>
                            </div>
                        </div>

                    </div>

                    <div className="flex flex-col items-center gap-4 py-4">
                        <button className="flex items-center justify-center size-16 rounded-full bg-[#B5C1A8] text-[#333333] shadow-lg shadow-[#B5C1A8]/30 transition-transform hover:scale-105 active:scale-95">
                            <span className="material-symbols-outlined text-3xl text-white">mic</span>
                        </button>
                        <p className="text-[#B5C1A8] text-base font-bold leading-normal text-center bg-white/60 px-4 py-2 rounded-full border border-[#E6DCC8] text-[#333333]/80">
                            Aap bol kar bhi bhasha chune sakte hain
                        </p>
                    </div>
                    <div className="pt-4">
                        <button onClick={() => {
                            updateOnboardingData('language', selected);
                            navigate('/onboarding/location');
                        }} className="w-full flex items-center justify-center gap-2 h-14 rounded-xl bg-[#9CAF88] hover:bg-[#8B9D78] text-[#333333] text-lg font-bold tracking-[0.015em] transition-colors shadow-lg shadow-[#9CAF88]/20">
                            <span>Aage Badhein</span>
                            <span className="opacity-80 text-sm font-normal">(Continue)</span>
                            <span className="material-symbols-outlined ml-1 text-xl">arrow_forward</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LanguageSelection;
