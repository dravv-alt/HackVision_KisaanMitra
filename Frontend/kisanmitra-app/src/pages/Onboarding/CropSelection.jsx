import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useOnboarding } from '../../context/OnboardingContext';

const CropSelection = () => {
    const navigate = useNavigate();
    const { onboardingData, updateOnboardingData } = useOnboarding();
    const [season, setSeason] = useState('Kharif');
    const [selectedCrops, setSelectedCrops] = useState(onboardingData.selectedCrops || ['wheat']); // Default Wheat selected per snippet

    const toggleCrop = (id) => {
        if (selectedCrops.includes(id)) {
            setSelectedCrops(selectedCrops.filter(c => c !== id));
        } else {
            setSelectedCrops([...selectedCrops, id]);
        }
    };

    const crops = [
        { id: 'wheat', name: 'Wheat', sub: 'Gehu', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDAxUvts4D-bAip0W0Eyy6H5gis0e-wzr8chpRYItc6-1Uo6JbKARtts_MclTvPo5bt6r1hxB5LHeUJg-f3U2MZ5P7r_SsZ9M3JwlDxlbCbnSI143ZEUmdstyZ3Lp0DQ4uBCV28obvfyq_G9F2gdY2tdX66kpGC6EX6a5ArDakT101onxub0-S5tTJT_FKRl5da_MmgBEz_2uuBBg8q1INWZr2tI-uUq0KhDZk5PWPX-rFd8pwl9C5p1PHOlQelZ_1xVbqMU7EWmjQ' },
        { id: 'cotton', name: 'Cotton', sub: 'Kapas', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuADdWPsAUVBoknkT81I5ZxPhjxZznJojCwrXLy6v9FJ5tRH7MjNeJSpuExgPC5aaZOgYNJWNEEkNE802b3a3bQBaorn_959vDU9N5aFzitaXl-Me0BHLwwTQKu4yXbkQRjktadUdc1WYFo8UjOzkW3vS8aQ8BSDHZeKq_0_3r3ntWNO8t5Vqb4Dtjo02998Ghi-51gpTsc6YdhSnA_6rQ__HDOngZR6No1STwCV9nM85LXpz26q6JQBgWOxMRcY0ldrnI7wnGRIHJA' },
        { id: 'rice', name: 'Rice', sub: 'Chawal', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAen8D1CLivsVfDnxsWVYNeLl8EBgvwQ0DwfHRv0rtpRlHWyzigG120B0sxuiZW0pucHxzVXytmn5Vwk51_MfCpy9akpTUU06o6hxqJL4s73o896ELLpxoufQvpGKGP-QvHpESrfB7ZMs7xYr0xwzM8eoukmoQSczpqfwJMpdqwdyE8ocCE-bPh0eSzCkmVmV-K9QOa4kXxenyxdS51T1alRmhnonbUDu01UrGzDiykJMAD8IMJtOxdyJWhOY5DucUvFefe9-Gn2mU' },
        { id: 'maize', name: 'Maize', sub: 'Makka', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuC55B9O-xFGj7Pa9d3gN4HkT9y0mtiB7ZOHyth87x9x9hKrGtllMbToQOH_OQUud2E1GZCm2WsnKClCADYlDiJKRVfCrzXZCNFITNiZ3Q6VnxYhU--Ocbg12al_PbUHP6bK30gK7aPQZoTjr3T4vqUvK4yW8FvFGXibEpFUR2Ny8c-x3yjHsqbpgwV_-W-D8Rnu2DZfEJ69VMINFa6wmI7-IIRL_vQhTVPsV-dDG_w34WULsMD21lWGUkbBhDfWIz2CGQh2xHGc8Zc' },
        { id: 'potato', name: 'Potato', sub: 'Aloo', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAzzJbioZWuFSoYhS209RZCu3XZCb_pT5UeCJC1Y1pIvIK0MZfOqVauOb9YG1Hr2kaqnfXAa5LhtOXqnlDDvsQ09hDKrZgYRIyTVctunfF_nTOoFTpwoDaFnmCUFtE0743J9z9zk_NSv5mZs3ka781qx9xUTSHxNdbB88I2C8cICHesmjjz-aYEVOwEh-a8aJhpFbHUz2M7hW4hbGSN7yNDu2ZjEMbYRKWluT_P1395c6yd7S2WLFoHndp99Q4Hu4_3PO-sCAjJcvw' },
    ];

    return (
        <div className="bg-[#F5F2E9] dark:bg-[#1C211B] text-[#2F3E32] dark:text-gray-100 font-['Work_Sans'] min-h-screen flex flex-col">
            <header className="sticky top-0 z-20 w-full bg-[#FEFDF5]/95 dark:bg-[#2A3329]/95 backdrop-blur border-b border-[#84A98C]/20 dark:border-gray-800">
                <div className="px-6 md:px-10 py-4 max-w-[1200px] mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className="size-8 text-[#84A98C]">
                            <svg className="h-full w-full" fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                                <path clipRule="evenodd" d="M47.2426 24L24 47.2426L0.757355 24L24 0.757355L47.2426 24ZM12.2426 21H35.7574L24 9.24264L12.2426 21Z" fill="currentColor" fillRule="evenodd"></path>
                            </svg>
                        </div>
                        <h2 className="text-xl font-bold leading-tight tracking-tight">KisanMitra</h2>
                    </div>
                    <button aria-label="Menu" className="flex items-center justify-center size-10 rounded-lg bg-[#84A98C]/10 dark:bg-gray-800 text-[#2F3E32] dark:text-gray-200 cursor-not-allowed opacity-70" disabled>
                        <span className="material-symbols-outlined">menu</span>
                    </button>
                </div>
            </header>
            <main className="flex-1 w-full max-w-[1200px] mx-auto px-4 md:px-10 py-8 relative">
                <div className="flex flex-col gap-2 mb-8 animate-fade-in-up">
                    <h1 className="text-3xl md:text-4xl font-black leading-tight tracking-tight text-[#2F3E32] dark:text-white">
                        Kaunse Fasal Ugayi Ja Rahi Hai?
                    </h1>
                    <p className="text-[#6B7C6E] dark:text-green-400 text-lg font-medium">
                        Which crops are you growing currently?
                    </p>
                </div>
                <div className="mb-8">
                    <div className="inline-flex bg-[#FEFDF5] dark:bg-[#2A3329] rounded-xl p-1 shadow-sm border border-[#84A98C]/10 dark:border-gray-800">
                        {['Kharif', 'Rabi', 'Zaid'].map((s) => (
                            <button
                                key={s}
                                onClick={() => setSeason(s)}
                                className={`px-6 py-2.5 rounded-lg font-medium transition-all duration-200 ${season === s ? 'bg-[#E3C565] text-[#2F3E32] font-bold shadow-sm' : 'text-[#6B7C6E] dark:text-gray-400 hover:text-[#2F3E32] dark:hover:text-white hover:bg-[#E3C565]/20'}`}
                            >
                                {s}
                            </button>
                        ))}
                    </div>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 mb-12">
                    {crops.map((crop) => (
                        <label key={crop.id} className="relative cursor-pointer group" onClick={() => toggleCrop(crop.id)}>
                            <div className={`flex flex-col h-full bg-[#FEFDF5] dark:bg-[#2A3329] border-2 rounded-2xl shadow-sm hover:shadow-md p-4 transition-all duration-200 group-hover:-translate-y-1 ${selectedCrops.includes(crop.id) ? 'border-[#84A98C] bg-[#F0F6F1]' : 'border-transparent'}`}>
                                <div className={`absolute top-3 right-3 size-6 rounded-full bg-[#84A98C] flex items-center justify-center transform transition-all duration-200 shadow-sm z-10 ${selectedCrops.includes(crop.id) ? 'opacity-100 scale-100' : 'opacity-0 scale-75'}`}>
                                    <span className="material-symbols-outlined text-sm font-bold text-white">check</span>
                                </div>
                                <div className="w-full aspect-square bg-gray-100 dark:bg-gray-800 rounded-xl mb-4 overflow-hidden relative">
                                    <div className="absolute inset-0 bg-cover bg-center" style={{ backgroundImage: `url('${crop.img}')` }}></div>
                                </div>
                                <div className="mt-auto">
                                    <h3 className="text-lg font-bold text-[#2F3E32] dark:text-white">{crop.name}</h3>
                                    <p className="text-sm text-[#6B7C6E] dark:text-gray-400">{crop.sub}</p>
                                </div>
                            </div>
                        </label>
                    ))}

                    <button className="relative cursor-pointer group flex flex-col h-full min-h-[220px] bg-[#FEFDF5] dark:bg-[#2A3329] border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-2xl hover:border-sky-300 hover:bg-sky-50 dark:hover:bg-sky-900/10 transition-all duration-200 items-center justify-center text-center p-4">
                        <div className="size-12 rounded-full bg-sky-100 dark:bg-sky-900 flex items-center justify-center mb-3 group-hover:bg-sky-200 transition-colors">
                            <span className="material-symbols-outlined text-sky-600 dark:text-sky-300 group-hover:text-sky-800">add</span>
                        </div>
                        <h3 className="text-lg font-bold text-[#2F3E32] dark:text-white">Add Another</h3>
                        <p className="text-sm text-[#6B7C6E] dark:text-gray-400">Aur jodein</p>
                    </button>

                </div>
                <div className="fixed bottom-24 right-6 md:right-10 z-30">
                    <button className="flex items-center justify-center size-14 bg-[#84A98C] hover:bg-[#6B8F73] text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-200 active:scale-95 group">
                        <span className="material-symbols-outlined text-[28px] group-hover:scale-110 transition-transform">mic</span>
                        <div className="absolute right-full mr-4 bg-black/80 text-white text-xs px-3 py-1.5 rounded opacity-0 group-hover:opacity-100 whitespace-nowrap transition-opacity pointer-events-none">
                            Voice Search
                        </div>
                    </button>
                </div>
            </main>
            <div className="sticky bottom-0 w-full bg-[#FEFDF5] dark:bg-[#2A3329] border-t border-[#84A98C]/10 dark:border-gray-800 p-4 z-20">
                <div className="max-w-[1200px] mx-auto flex flex-col-reverse sm:flex-row items-center justify-between gap-4">
                    <div className="text-sm text-[#6B7C6E] dark:text-gray-400 font-medium">
                        <span className="font-bold text-[#84A98C]">{selectedCrops.length}</span> crop{selectedCrops.length !== 1 ? 's' : ''} selected
                    </div>
                    <div className="flex items-center gap-4 w-full sm:w-auto">
                        <button className="hidden sm:flex px-6 py-3 rounded-xl text-[#6B7C6E] dark:text-gray-300 font-bold hover:bg-black/5 dark:hover:bg-gray-800 transition-colors">
                            Skip
                        </button>
                        <button onClick={() => {
                            updateOnboardingData('selectedCrops', selectedCrops);
                            navigate('/onboarding/summary');
                        }} className="flex-1 sm:flex-none w-full sm:w-auto px-10 py-3 rounded-xl bg-[#84A98C] hover:bg-[#6B8F73] text-white font-bold text-base shadow-md hover:shadow-lg transition-all duration-200 flex items-center justify-center gap-2">
                            Continue
                            <span className="material-symbols-outlined text-xl">arrow_forward</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CropSelection;
