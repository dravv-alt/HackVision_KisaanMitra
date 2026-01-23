import React from 'react';
import { useNavigate } from 'react-router-dom';

const LocationSetup = () => {
    const navigate = useNavigate();

    return (
        <div className="bg-[#F9F7F2] dark:bg-[#1C1C1A] min-h-screen flex flex-col font-display overflow-x-hidden selection:bg-[#A3B899]/30 font-['Work_Sans']">
            <div className="w-full flex justify-center bg-[#F9F7F2] dark:bg-[#1C1C1A] border-b border-[#E8E4D8] dark:border-[#333330]">
                <div className="w-full max-w-[600px] flex items-center justify-between px-6 py-4">
                    <div className="flex items-center gap-3 text-[#3C3830] dark:text-white">
                        <div className="size-6 text-[#A3B899]">
                            <svg className="w-full h-full" fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                                <path clipRule="evenodd" d="M47.2426 24L24 47.2426L0.757355 24L24 0.757355L47.2426 24ZM12.2426 21H35.7574L24 9.24264L12.2426 21Z" fill="currentColor" fillRule="evenodd"></path>
                            </svg>
                        </div>
                        <h2 className="text-[#3C3830] dark:text-[#E8F3E7] text-xl font-bold tracking-tight">KisanMitra</h2>
                    </div>
                    <button aria-label="Menu disabled" className="flex items-center justify-center text-[#8D7B68] opacity-50 cursor-not-allowed">
                        <span className="material-symbols-outlined text-3xl">menu</span>
                    </button>
                </div>
            </div>
            <main className="flex-grow flex flex-col items-center px-4 py-6 w-full">
                <div className="w-full max-w-[600px] flex flex-col gap-6">
                    <div className="flex flex-col gap-2 pt-4 px-2">
                        <h1 className="text-[#3C3830] dark:text-white text-[32px] font-bold leading-[1.1] tracking-tight">
                            Aapka Gaon Kahan Hai?
                        </h1>
                        <p className="text-[#6B8066] text-lg font-medium">
                            Where is your village?
                        </p>
                    </div>
                    <div className="bg-[#F7F3E8] dark:bg-[#2A2210] rounded-xl shadow-sm border border-[#EBE4D1] dark:border-[#3E3320] overflow-hidden">
                        <div className="px-5 py-4 border-b border-[#EBE4D1] dark:border-[#3E3320] flex items-center gap-2">
                            <span className="material-symbols-outlined text-[#C7B066] dark:text-[#FCD34D]" style={{ fontSize: '20px' }}>my_location</span>
                            <h3 className="text-[#5C5142] dark:text-[#FCD34D] text-sm font-bold uppercase tracking-wider">Detected Location</h3>
                        </div>
                        <div className="px-5 py-2">
                            <div className="grid grid-cols-[30%_1fr] gap-y-4 py-4">
                                <div className="flex flex-col justify-center">
                                    <p className="text-[#8D7B68] dark:text-[#9CA3AF] text-sm font-medium">State</p>
                                </div>
                                <div className="flex flex-col justify-center">
                                    <p className="text-[#3C3830] dark:text-white text-base font-semibold">Maharashtra</p>
                                </div>
                                <div className="col-span-2 border-t border-[#EBE4D1] dark:border-[#3E3320]"></div>
                                <div className="flex flex-col justify-center">
                                    <p className="text-[#8D7B68] dark:text-[#9CA3AF] text-sm font-medium">District</p>
                                </div>
                                <div className="flex flex-col justify-center">
                                    <p className="text-[#3C3830] dark:text-white text-base font-semibold">Pune</p>
                                </div>
                                <div className="col-span-2 border-t border-[#EBE4D1] dark:border-[#3E3320]"></div>
                                <div className="flex flex-col justify-center">
                                    <p className="text-[#8D7B68] dark:text-[#9CA3AF] text-sm font-medium">Village</p>
                                </div>
                                <div className="flex flex-col justify-center">
                                    <p className="text-[#3C3830] dark:text-white text-base font-semibold">Haveli</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="flex gap-3 px-2">
                        <span className="material-symbols-outlined text-[#6B8066] shrink-0" style={{ fontSize: '24px' }}>info</span>
                        <p className="text-[#59554F] dark:text-[#D1D5DB] text-sm leading-relaxed">
                            This information helps us provide accurate weather forecasts and Mandi prices specifically for your area.
                        </p>
                    </div>
                    <div className="flex flex-col gap-3 mt-4">
                        <button onClick={() => navigate('/onboarding/soil')} className="w-full h-14 bg-[#A3B899] hover:bg-[#8DA385] active:bg-[#7A9072] text-[#1F261E] rounded-lg text-lg font-bold shadow-sm transition-colors flex items-center justify-center gap-2">
                            <span className="material-symbols-outlined">check_circle</span>
                            Confirm Location
                        </button>
                        <button className="w-full h-12 bg-transparent border-2 border-[#D1CEC7] dark:border-[#4B5563] text-[#6B5D4D] dark:text-[#9CA3AF] hover:border-[#8D7B68] hover:text-[#4A3B22] dark:hover:text-white rounded-lg text-base font-semibold transition-colors flex items-center justify-center gap-2">
                            Change Manually
                        </button>
                    </div>
                </div>
            </main>
            <div className="fixed bottom-8 right-8 z-50">
                <button aria-label="Voice Input" className="floating-action-btn size-16 rounded-full bg-[#A3B899] text-[#1F261E] flex items-center justify-center hover:brightness-105 focus:outline-none focus:ring-4 focus:ring-[#A3B899]/30 shadow-lg transition-transform active:scale-95">
                    <span className="material-symbols-outlined" style={{ fontSize: '32px' }}>mic</span>
                </button>
            </div>
        </div>
    );
};

export default LocationSetup;
