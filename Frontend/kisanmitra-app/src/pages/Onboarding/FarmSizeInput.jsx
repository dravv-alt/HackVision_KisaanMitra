import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const FarmSizeInput = () => {
    const navigate = useNavigate();
    const [size, setSize] = useState('');
    const [unit, setUnit] = useState('Bigha'); // Default Bigha

    return (
        <div className="bg-[#F2EFE7] dark:bg-[#1C1F1C] min-h-screen w-full flex flex-col font-['Space_Grotesk'] selection:bg-[#9AB8A0]/30 overflow-hidden">
            <style>{`
                input[type=number]::-webkit-inner-spin-button, 
                input[type=number]::-webkit-outer-spin-button { 
                    -webkit-appearance: none; 
                    margin: 0; 
                }
                .input-underline {
                    position: absolute;
                    bottom: 0;
                    left: 0;
                    right: 0;
                    height: 2px;
                    background-color: #E8E6DC;
                    transition: all 0.3s ease;
                }
                input:focus ~ .input-underline {
                    background-color: #9AB8A0;
                    height: 3px;
                }
            `}</style>
            <div className="layout-container flex h-full grow flex-col items-center justify-center p-4 sm:p-8">
                <div className="relative w-full max-w-[440px] h-[85vh] max-h-[840px] flex flex-col bg-[#FAF9F6] dark:bg-[#232623] rounded-[32px] shadow-2xl border-[6px] border-white dark:border-[#222] overflow-hidden">
                    <header className="flex items-center justify-between px-6 py-5 z-10">
                        <button aria-label="Menu" className="size-10 flex items-center justify-center rounded-full text-[#657A69]/60 cursor-not-allowed hover:bg-transparent" disabled>
                            <span className="material-symbols-outlined" style={{ fontSize: '28px' }}>menu</span>
                        </button>
                        <div className="flex items-center gap-2 select-none">
                            <span className="material-symbols-outlined text-[#85A38B] dark:text-[#9AB8A0]">agriculture</span>
                            <h2 className="text-[#1E281F] dark:text-white text-lg font-bold tracking-tight">KisanMitra</h2>
                        </div>
                        <div className="size-10"></div>
                    </header>
                    <main className="flex-1 flex flex-col items-center px-6 relative overflow-y-auto no-scrollbar">
                        <div className="w-full flex-1 flex flex-col items-center justify-center -mt-10">
                            <h1 className="text-[#1E281F] dark:text-white text-[32px] sm:text-[36px] font-bold leading-[1.15] text-center mb-10 tracking-tight">
                                Aapki Zameen Kitni Hai?
                            </h1>
                            <div className="w-full max-w-[240px] relative mb-10 group">
                                <input
                                    className="w-full bg-transparent border-none text-center text-7xl sm:text-8xl font-bold text-[#1E281F] dark:text-white placeholder:text-[#CEDBD0] dark:placeholder:text-[#333] focus:outline-none focus:ring-0 py-2 font-display"
                                    placeholder="0"
                                    type="number"
                                    value={size}
                                    onChange={(e) => setSize(e.target.value)}
                                    autoFocus
                                />
                                <div className="input-underline"></div>
                            </div>
                            <div className="w-full max-w-[260px] bg-[#E8E6DC] dark:bg-[#252f26] p-1.5 rounded-xl flex items-center mb-14">
                                <label className="flex-1 cursor-pointer h-11 relative" onClick={() => setUnit('Bigha')}>
                                    <div className={`absolute inset-0 flex items-center justify-center rounded-lg text-sm font-bold transition-all duration-200 z-10 ${unit === 'Bigha' ? 'text-[#1E281F]' : 'text-[#657A69] dark:text-gray-400'}`}>
                                        Bigha
                                    </div>
                                    <div className={`absolute inset-0 rounded-lg transition-all duration-200 ${unit === 'Bigha' ? 'bg-[#9AB8A0] shadow-sm' : 'bg-transparent'}`}></div>
                                </label>
                                <label className="flex-1 cursor-pointer h-11 relative" onClick={() => setUnit('Acre')}>
                                    <div className={`absolute inset-0 flex items-center justify-center rounded-lg text-sm font-bold transition-all duration-200 z-10 ${unit === 'Acre' ? 'text-[#1E281F]' : 'text-[#657A69] dark:text-gray-400'}`}>
                                        Acre
                                    </div>
                                    <div className={`absolute inset-0 rounded-lg transition-all duration-200 ${unit === 'Acre' ? 'bg-[#9AB8A0] shadow-sm' : 'bg-transparent'}`}></div>
                                </label>
                            </div>
                            <div className="flex flex-col items-center gap-4 animate-fade-in-up">
                                <button className="group relative size-16 flex items-center justify-center bg-white dark:bg-[#252f26] rounded-full shadow-[0_8px_30px_-4px_rgba(101,122,105,0.1)] hover:shadow-[0_0_20px_rgba(154,184,160,0.3)] transition-all duration-300 hover:scale-105 active:scale-95 border border-[#E8E6DC] dark:border-[#333]">
                                    <span className="material-symbols-outlined text-[32px] text-[#9AB8A0] group-hover:text-[#85A38B] transition-colors">mic</span>
                                    <div className="absolute inset-0 rounded-full border border-[#9AB8A0]/30 scale-110 opacity-0 group-hover:opacity-100 group-hover:scale-125 transition-all duration-500"></div>
                                </button>
                                <p className="text-[#657A69] dark:text-[#8aa] text-base font-medium text-center">
                                    Bol kar bhi bata sakte hain
                                </p>
                            </div>
                        </div>
                    </main>
                    <div className="p-6 pb-8 bg-gradient-to-t from-[#FAF9F6] via-[#FAF9F6] to-transparent dark:from-[#232623] dark:via-[#232623] w-full z-20">
                        <button onClick={() => navigate('/onboarding/crops')} className="w-full h-14 bg-[#9AB8A0] hover:bg-[#85A38B] text-[#1E281F] text-lg font-bold rounded-xl shadow-lg shadow-[#9AB8A0]/25 transition-all transform active:scale-[0.98] flex items-center justify-center gap-2 group">
                            Continue
                            <span className="material-symbols-outlined text-[20px] group-hover:translate-x-1 transition-transform">arrow_forward</span>
                        </button>
                    </div>
                </div>
                <div className="mt-6 text-[#657A69] text-sm hidden sm:block">
                    Press <span className="font-mono bg-white dark:bg-[#222] px-1.5 py-0.5 rounded text-xs border border-[#E8E6DC] dark:border-[#444] text-[#1E281F]">Enter</span> to continue
                </div>
            </div>
        </div>
    );
};

export default FarmSizeInput;
