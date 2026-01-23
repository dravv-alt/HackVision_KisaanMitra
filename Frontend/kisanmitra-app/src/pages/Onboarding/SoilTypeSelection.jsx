import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useOnboarding } from '../../context/OnboardingContext';

const SoilTypeSelection = () => {
    const navigate = useNavigate();
    const { onboardingData, updateOnboardingData } = useOnboarding();
    const [selected, setSelected] = useState(onboardingData.soilType || '');

    const soilTypes = [
        {
            value: 'alluvial',
            title: 'Alluvial (Jalodh)',
            desc: 'Found near rivers, highly fertile.',
            img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuACmU_ScrLyd6JEWguS4AdJrMHun8ee4gOcgOuDzCUIJz97jr3gO74wbawjl_6l3toWFZpM0OPIOBRdBAB4ZW0JUty1ErdjnirrrsFXEdJ_El6w0MoK9LkPhhjFV6-iMPZApeZsyAH5TScj-aVaf2p7gOmbwyRKG38ZL39bNJuddV_SNJjXXCjmlCvYKQDo7vUzi_1SYBc9TwFhqOjV2YKdI_H_UtcEUgOkQM_VsicWcy2hRRhF7zaG0pdzLuYOqSAdKd-5wWGy4SU'
        },
        {
            value: 'black',
            title: 'Black (Kaali)',
            desc: 'Dark color, retains moisture well.',
            img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCWKapg48fxywJg5LRHrg9gxsI2cYPiJtNr6NS36SDk71AhcSn23JgoUzxVvlrk68rTW-U6DKhGb_I0HDfDVQgIss06v1aVpPPA7AaoD8bf5r__NB1OJtUHLJY6FCCp9Qd839rH3xOPCnbTrxID8ZALI0CT90SrH7OtSVshcmI3h6BYhCWHQUPlLQBHXMhZI9yS7NfIwV07tjYc_jBmC3QS6FY5825KSONfBa8PJxLChI3h6BYhCWHQUPlLQBHXMhZI9yS7NfIwV07tjYc_jBmC3QS6FY5825KSONfBa8PJxLChI3MZ6y4DkLwJ2XclgrXyxAgAPDyC-jJ5E' // Shortened URI in original snippet looked suspicious but I'll use the one from the file view
        },
        {
            value: 'red',
            title: 'Red (Laal)',
            desc: 'Rich in iron, reddish texture.',
            img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCINpcVeJfgOGisTNqO0m4p1GFvilzv2F1k_0C5VibmzYlCI0FyUYPxOFuTMRZqFFeWhtw7_VdRv1IOvHVkrpyX1ei-ZOg7DWgFT1Q9-bHYuXxUZOmzuCEishSPRYkv5dkTeLJ7QEpMjnfllsI5wmSIeDjar7QdI6bOU-0ADgpXhI2jkmhAAckTYZTcc-7yzsNMrNtZzdezfqL38hJAoMmq-UaJCyv13iEU1dMinXUZeZPLDMOq-Xu3NggHcy8ITKqvPU1ogm-V0nA'
        },
        {
            value: 'sandy',
            title: 'Sandy (Retili)',
            desc: 'Loose particles, drains water fast.',
            img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCqG499qm6AfLZ7VP92vL41J5W4rv6vr4Mh9nYsUgCnzEPmuhDfw1JCPVW_A_cQKIUsf8dCgy9MtHTKuKHXf4IpYnnBCoddFSacifxZhN7y-ddHjYLpRwfG_KEu6prfZRkxG9XF7W_weG1F1yi_fZgEWrwYYDVB6zHgdeQKoGlmlO1aKv0GxY9wXjfzwS6JE4TrbLwXzp54gVpgOEB3CoKx2aKjBp014eMPJLMlTLy5lfVLfySyaZYmodaT25NNWpStZkMkY54mNeQ'
        },
        {
            value: 'clay',
            title: 'Clay (Chickni)',
            desc: 'Sticky when wet, hard when dry.',
            img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAVeyvDj7cb_dIyYkED6hpMdAyAQ_lkJDPcF26FkGEyIZ2NdKyQNCVMDpYPrY6rSlnLK09AbcerhQI_gPE4vPIzBVHpwg_eKHfGd8PXKvw62XLA2h8cvGdzFr7jPhT9dJD9HZ-Fp0Bxea30BVv3hriB2FMUd2v7yGB7PdgkRncuySTY1rpSdA--C_p_g7E3LksS279Y4IuPTD4yqIZf8Sh1CMl-D0W3OzQiTM3jA52gxnkGcuJEExu9w9BxPzipvZ6ffqXRF34FlBg'
        }
    ];

    // Correcting the Black Soil image URL from the previous step which might have been truncated during thought process
    const blackSoilImg = 'https://lh3.googleusercontent.com/aida-public/AB6AXuCWKapg48fxywJg5LRHrg9gxsI2cYPiJtNr6NS36SDk71AhcSn23JgoUzxVvlrk68rTW-U6DKhGb_I0HDfDVQgIss06v1aVpPPA7AaoD8bf5r__NB1OJtUHLJY6FCCp9Qd839rH3xOPCnbTrxID8ZALI0CT90SrH7OtSVshcmI3h6BYhCWHQUPlLQBHXMhZI9yS7NfIwV07tjYc_jBmC3QS6FY5825KSONfBa8PJxLChI30MZ6y4DkLwJ2XclgrXyxAgAPDyC-jJ5E';
    soilTypes[1].img = blackSoilImg;

    return (
        <div className="bg-[#F9F6F0] dark:bg-[#1A1D1A] text-[#2C3329] dark:text-white font-['Lexend'] min-h-screen flex flex-col overflow-x-hidden">
            <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#E6E0D0] dark:border-b-[#2a3825] px-6 lg:px-40 py-4 bg-[#FDFBF7] dark:bg-[#1a2615]">
                <div className="flex items-center gap-3">
                    <div className="size-8 text-[#84A98C] flex items-center justify-center bg-[#84A98C]/20 rounded-full p-1.5">
                        <span className="material-symbols-outlined text-2xl font-bold">agriculture</span>
                    </div>
                    <h2 className="text-[#2C3329] dark:text-white text-xl font-bold tracking-tight">KisanMitra</h2>
                </div>
                <button className="flex items-center gap-2 rounded-xl bg-[#E0F0F2] dark:bg-[#2a3825] px-3 py-2 text-sm font-semibold transition-colors hover:bg-[#D1E6EA] dark:hover:bg-[#364630] text-[#2C3329] dark:text-white">
                    <span className="material-symbols-outlined text-lg">translate</span>
                    <span>English / हिंदी</span>
                </button>
            </header>
            <main className="flex-1 flex justify-center py-8 px-4 lg:px-0 bg-[#F9F6F0] dark:bg-[#1A1D1A]">
                <div className="flex flex-col w-full max-w-[960px] gap-8">
                    <div className="flex flex-col gap-3 px-4">
                        <div className="flex justify-between items-center">
                            <p className="text-[#2C3329] dark:text-white text-sm font-medium">Step 2 of 4</p>
                            <span className="text-xs text-gray-500 dark:text-gray-400">Onboarding</span>
                        </div>
                        <div className="h-2 w-full rounded-full bg-[#E6E0D0] dark:bg-[#2a3825]">
                            <div className="h-2 rounded-full bg-[#84A98C]" style={{ width: '50%' }}></div>
                        </div>
                    </div>
                    <div className="flex flex-col gap-2 px-4">
                        <h1 className="text-3xl lg:text-4xl font-black leading-tight tracking-tight text-[#2C3329] dark:text-white">
                            Aapki Mitti Ka Prakar
                        </h1>
                        <p className="text-[#6E9175] dark:text-[#8ea885] text-lg font-normal">
                            Select the soil type that matches your farm
                        </p>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 px-4 pb-24">

                        {soilTypes.map((soil) => (
                            <label key={soil.value} className="group relative cursor-pointer" onClick={() => setSelected(soil.value)}>
                                <div className={`flex flex-col h-full rounded-2xl bg-[#EFE6D8] dark:bg-[#2a2720] border-2 p-4 transition-all hover:shadow-md ${selected === soil.value ? 'border-[#84A98C] bg-[#84A98C]/10 dark:bg-green-900/20' : 'border-transparent'}`}>
                                    <div className="mb-4 aspect-video w-full overflow-hidden rounded-xl bg-[#E3DACB] dark:bg-[#38342a]">
                                        <div
                                            className="h-full w-full bg-cover bg-center transition-transform duration-500 group-hover:scale-105"
                                            style={{ backgroundImage: `url('${soil.img}')` }}
                                        ></div>
                                    </div>
                                    <div className="flex flex-col gap-1">
                                        <h3 className="text-lg font-bold text-[#2C3329] dark:text-white">{soil.title}</h3>
                                        <p className="text-sm text-gray-600 dark:text-gray-400">{soil.desc}</p>
                                    </div>
                                    <div className={`absolute top-4 right-4 transition-opacity ${selected === soil.value ? 'opacity-100' : 'opacity-0'}`}>
                                        <div className="flex h-6 w-6 items-center justify-center rounded-full bg-[#84A98C] text-[#2C3329]">
                                            <span className="material-symbols-outlined text-sm font-bold">check</span>
                                        </div>
                                    </div>
                                </div>
                            </label>
                        ))}

                        {/* Pata Nahi Option */}
                        <label className="group relative cursor-pointer" onClick={() => setSelected('dont-know')}>
                            <div className={`flex flex-col h-full rounded-2xl bg-[#EFE6D8] dark:bg-[#3a352b] border-2 border-dashed p-4 transition-all hover:bg-[#E5DCCB] dark:hover:bg-[#453f33] hover:shadow-md ${selected === 'dont-know' ? 'border-[#84A98C] border-solid bg-[#84A98C]/10 dark:bg-green-900/20' : 'border-[#D6B875] dark:border-[#6b5f4d]'}`}>
                                <div className="mb-4 flex aspect-video w-full items-center justify-center rounded-xl bg-[#E5DCCB] dark:bg-[#2e2a22]">
                                    <span className="material-symbols-outlined text-6xl text-[#D6B875] dark:text-[#a89b85]">location_on</span>
                                </div>
                                <div className="flex flex-col gap-1">
                                    <h3 className="text-lg font-bold text-[#2C3329] dark:text-white">Pata Nahi</h3>
                                    <p className="text-sm text-[#84A98C] font-medium leading-snug">Hum location se andaza laga lenge</p>
                                </div>
                                <div className={`absolute top-4 right-4 transition-opacity ${selected === 'dont-know' ? 'opacity-100' : 'opacity-0'}`}>
                                    <div className="flex h-6 w-6 items-center justify-center rounded-full bg-[#84A98C] text-[#2C3329]">
                                        <span className="material-symbols-outlined text-sm font-bold">check</span>
                                    </div>
                                </div>
                            </div>
                        </label>

                    </div>
                </div>
            </main>
            <button className="fixed bottom-24 right-6 lg:right-12 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-[#FDFBF7] dark:bg-[#2a3825] text-[#84A98C] shadow-lg border border-[#84A98C]/30 transition-transform hover:scale-110 active:scale-95 focus:outline-none focus:ring-4 focus:ring-[#84A98C]/20">
                <span className="material-symbols-outlined text-3xl">mic</span>
            </button>
            <div className="fixed bottom-0 left-0 right-0 border-t border-[#E6E0D0] dark:border-[#2a3825] bg-[#F9F6F0]/95 dark:bg-[#152111]/95 px-4 py-4 backdrop-blur-sm">
                <div className="mx-auto flex w-full max-w-[960px] justify-center">
                    <button onClick={() => {
                        updateOnboardingData('soilType', selected);
                        navigate('/onboarding/size');
                    }} className="flex h-12 w-full max-w-[400px] cursor-pointer items-center justify-center gap-2 rounded-xl bg-[#84A98C] px-8 text-base font-bold tracking-wide text-[#2C3329] shadow-sm transition-all hover:bg-[#6E9175] hover:shadow-md active:scale-[0.98]">
                        <span>Aage Badhein (Continue)</span>
                        <span className="material-symbols-outlined text-lg">arrow_forward</span>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default SoilTypeSelection;
