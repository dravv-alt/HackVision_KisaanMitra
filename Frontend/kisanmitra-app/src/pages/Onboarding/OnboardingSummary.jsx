import React from 'react';
import { useNavigate } from 'react-router-dom';

const OnboardingSummary = () => {
    const navigate = useNavigate();

    return (
        <div className="bg-[#F7F5EF] dark:bg-[#1C1C1C] text-[#2C2C2C] dark:text-gray-100 flex flex-col min-h-screen font-['Manrope']">
            <header className="sticky top-0 z-50 w-full bg-[#F7F5EF]/90 dark:bg-[#1C1C1C]/90 backdrop-blur-md border-b border-[#EBE5D5] dark:border-[#333]">
                <div className="max-w-[960px] mx-auto px-4 sm:px-10 py-3 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className="size-8 flex items-center justify-center text-[#99AF93]">
                            <span className="material-symbols-outlined text-3xl">agriculture</span>
                        </div>
                        <h2 className="text-lg font-bold leading-tight tracking-[-0.015em] text-[#2C2C2C] dark:text-white">KisanMitra</h2>
                    </div>
                    <button aria-label="Menu disabled" className="flex items-center justify-center size-10 rounded-full bg-[#EBE5D5] dark:bg-[#333] text-[#2C2C2C]/40 cursor-not-allowed opacity-60">
                        <span className="material-symbols-outlined">menu</span>
                    </button>
                </div>
            </header>
            <main className="flex-grow flex flex-col items-center justify-start py-8 px-4 sm:px-6">
                <div className="w-full max-w-[640px] flex flex-col gap-6">
                    <div className="flex flex-col gap-2 text-center sm:text-left">
                        <h1 className="text-4xl font-black leading-tight tracking-[-0.033em] text-[#2C2C2C] dark:text-white">
                            Aapki Jankari
                        </h1>
                        <p className="text-[#2C2C2C]/70 dark:text-gray-400 text-base font-normal">
                            Please review your details below before we proceed.
                        </p>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div className="bg-[#FFF9E6] dark:bg-[#2D2D2D] border border-[#F0E6CC] dark:border-[#404040] p-5 rounded-2xl flex flex-col gap-3 shadow-sm transition-transform hover:scale-[1.01]">
                            <div className="flex items-center justify-between">
                                <span className="text-[#2C2C2C]/80 dark:text-gray-300 text-sm font-semibold uppercase tracking-wider">Language</span>
                                <span className="material-symbols-outlined text-[#2C2C2C]/60 dark:text-gray-300">translate</span>
                            </div>
                            <p className="text-[#2C2C2C] dark:text-white text-xl font-bold">Hindi</p>
                        </div>
                        <div className="bg-[#FFF9E6] dark:bg-[#2D2D2D] border border-[#F0E6CC] dark:border-[#404040] p-5 rounded-2xl flex flex-col gap-3 shadow-sm transition-transform hover:scale-[1.01]">
                            <div className="flex items-center justify-between">
                                <span className="text-[#2C2C2C]/80 dark:text-gray-300 text-sm font-semibold uppercase tracking-wider">Location</span>
                                <span className="material-symbols-outlined text-[#2C2C2C]/60 dark:text-gray-300">location_on</span>
                            </div>
                            <div className="flex flex-col">
                                <p className="text-[#2C2C2C] dark:text-white text-lg font-bold leading-snug">Village Rampur</p>
                                <p className="text-[#2C2C2C]/70 dark:text-white/70 text-sm">Dist. Patna</p>
                            </div>
                        </div>
                        <div className="bg-[#FFF9E6] dark:bg-[#2D2D2D] border border-[#F0E6CC] dark:border-[#404040] p-5 rounded-2xl flex flex-col gap-3 shadow-sm transition-transform hover:scale-[1.01]">
                            <div className="flex items-center justify-between">
                                <span className="text-[#2C2C2C]/80 dark:text-gray-300 text-sm font-semibold uppercase tracking-wider">Soil Type</span>
                                <span className="material-symbols-outlined text-[#2C2C2C]/60 dark:text-gray-300">compost</span>
                            </div>
                            <p className="text-[#2C2C2C] dark:text-white text-lg font-bold">Loamy Soil (Doamat)</p>
                        </div>
                        <div className="bg-[#FFF9E6] dark:bg-[#2D2D2D] border border-[#F0E6CC] dark:border-[#404040] p-5 rounded-2xl flex flex-col gap-3 shadow-sm transition-transform hover:scale-[1.01]">
                            <div className="flex items-center justify-between">
                                <span className="text-[#2C2C2C]/80 dark:text-gray-300 text-sm font-semibold uppercase tracking-wider">Farm Size</span>
                                <span className="material-symbols-outlined text-[#2C2C2C]/60 dark:text-gray-300">square_foot</span>
                            </div>
                            <p className="text-[#2C2C2C] dark:text-white text-xl font-bold">5 Acres</p>
                        </div>
                        <div className="bg-[#FFF9E6] dark:bg-[#2D2D2D] border border-[#F0E6CC] dark:border-[#404040] p-5 rounded-2xl flex flex-col gap-3 shadow-sm sm:col-span-2 transition-transform hover:scale-[1.01]">
                            <div className="flex items-center justify-between">
                                <span className="text-[#2C2C2C]/80 dark:text-gray-300 text-sm font-semibold uppercase tracking-wider">Selected Crops</span>
                                <span className="material-symbols-outlined text-[#2C2C2C]/60 dark:text-gray-300">grass</span>
                            </div>
                            <div className="flex flex-wrap gap-2 mt-1">
                                <span className="inline-flex items-center px-3 py-1 rounded-full bg-white/60 dark:bg-black/20 text-[#2C2C2C] dark:text-white text-sm font-bold border border-white/40">
                                    Wheat
                                </span>
                                <span className="inline-flex items-center px-3 py-1 rounded-full bg-white/60 dark:bg-black/20 text-[#2C2C2C] dark:text-white text-sm font-bold border border-white/40">
                                    Mustard
                                </span>
                            </div>
                        </div>
                    </div>
                    <div className="mt-4 flex items-end gap-4 animate-fade-in-up">
                        <div className="relative w-12 h-12 shrink-0">
                            <div className="w-full h-full rounded-full bg-[#E8EFE9] dark:bg-green-900 flex items-center justify-center border-2 border-white dark:border-[#1C1C1C] shadow-sm">
                                <span className="material-symbols-outlined text-[#99AF93] text-2xl">smart_toy</span>
                            </div>
                            <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-[#99AF93] rounded-full border-2 border-white dark:border-[#1C1C1C]"></div>
                        </div>
                        <div className="flex flex-col gap-1 items-start max-w-[85%]">
                            <span className="text-[#2C2C2C]/70 dark:text-gray-400 text-xs font-semibold ml-1">KisanMitra AI</span>
                            <div className="rounded-2xl rounded-bl-none px-5 py-3 bg-[#E8EFE9] dark:bg-[#1e2e1b] text-[#2C2C2C] dark:text-white shadow-sm">
                                <p className="text-base font-medium leading-relaxed">
                                    Kya main is jankari ke saath aage badhun? <br />
                                    <span className="text-sm opacity-70 font-normal italic">(Shall I proceed with this info?)</span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
            <div className="sticky bottom-0 z-40 w-full bg-[#F7F5EF]/90 dark:bg-[#1C1C1C]/90 backdrop-blur-lg border-t border-[#EBE5D5] dark:border-[#333] py-4 px-4">
                <div className="max-w-[640px] mx-auto flex flex-row items-center justify-between gap-4">
                    <button className="group flex items-center justify-center size-14 rounded-full bg-white dark:bg-[#1e2e1b] border-2 border-[#99AF93] text-[#99AF93] hover:bg-[#99AF93] hover:text-[#2C2C2C] shadow-lg transition-all duration-300 shrink-0">
                        <span className="material-symbols-outlined text-3xl group-hover:scale-110 transition-transform">mic</span>
                    </button>
                    <button onClick={() => navigate('/dashboard')} className="flex-1 flex items-center justify-center h-14 rounded-full bg-[#99AF93] hover:bg-[#869C80] active:scale-[0.98] text-[#2C2C2C] text-lg font-bold shadow-lg shadow-[#99AF93]/20 transition-all duration-200 gap-2">
                        <span>Confirm & Start</span>
                        <span className="material-symbols-outlined">arrow_forward</span>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default OnboardingSummary;
