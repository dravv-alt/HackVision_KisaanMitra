import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const navigate = useNavigate();
    const [phone, setPhone] = useState('');

    const handleSendOtp = () => {
        if (phone.length === 10) {
            // Proceed to Language Selection directly for this demo, or add OTP step if desired.
            // Given the assets, we'll flow to Language.
            navigate('/onboarding/language');
        } else {
            alert("Please enter a valid 10-digit number");
        }
    };

    return (
        <div className="bg-[#F2EEE5] dark:bg-[#21211F] font-['Manrope'] text-[#2D332F] dark:text-[#E0DDD5] min-h-screen flex flex-col transition-colors duration-200">
            <div className="relative flex flex-col min-h-screen w-full overflow-x-hidden">
                <div
                    className="absolute inset-0 z-0 opacity-10 pointer-events-none bg-cover bg-center mix-blend-multiply"
                    data-alt="Abstract minimalist texture of green agricultural fields"
                    style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuBl_f3qSK0RMDMODgrAfBARbyTI9BT9FcScxqNLXw_K-_HBDESMEcc3lCnIWYLZ7_P0EI0R21zRMoGtRbKOgBxfPYzO69psY9v-YYya5fSPxQhEz8t6t70c9338kGKS4wgQHd5dKzHjddn3nsv_84ZyZ-M448YrdIn-p7fa5587X2T3204C0kofQzt9GHU3pWjEP36h-M_JHpI4AbprhoKAXXmzFwdMumrwaJvb7wQ2IGl_W_VYtn9Fqzgw5mQZsguTEftjmq0dm7Y')" }}
                >
                </div>
                <div className="z-10 flex flex-col flex-grow items-center justify-center p-4 sm:p-6 md:p-8">
                    <div className="w-full max-w-[480px] bg-[#FDFBF7] dark:bg-[#2E2D29] rounded-2xl shadow-xl overflow-hidden flex flex-col min-h-[600px] border border-[#E3DED1] dark:border-[#3E3C36]">
                        <header className="flex items-center justify-between px-6 py-5 border-b border-[#E3DED1] dark:border-[#3E3C36]">
                            <button aria-label="Menu disabled" className="text-[#7A8279] cursor-not-allowed opacity-50">
                                <span className="material-symbols-outlined text-3xl">menu</span>
                            </button>
                            <div className="flex items-center gap-2">
                                <div className="size-8 text-[#99B898] flex items-center justify-center">
                                    <span className="material-symbols-outlined text-4xl fill-1">agriculture</span>
                                </div>
                            </div>
                            <div className="w-8"></div>
                        </header>
                        <div className="flex-1 flex flex-col px-8 py-8 gap-8">
                            <div className="text-center flex flex-col gap-2 mt-4">
                                <h1 className="text-[#2D332F] dark:text-white text-3xl sm:text-4xl font-extrabold leading-tight tracking-tight">
                                    Welcome to <span className="text-[#99B898]">KisanMitra</span>
                                </h1>
                                <p className="text-[#7A8279] dark:text-gray-400 text-lg font-medium">
                                    Aapka kheti ka saathi
                                </p>
                            </div>
                            <div className="flex flex-col gap-6 mt-4">
                                <div className="flex flex-col gap-2">
                                    <label className="text-[#2D332F] dark:text-gray-200 text-base font-semibold ml-1" htmlFor="phone">
                                        Enter your mobile number
                                    </label>
                                    <div className="relative group">
                                        <div className="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
                                            <span className="text-[#7A8279] font-medium">+91</span>
                                            <div className="h-6 w-px bg-[#B0C4C9] mx-3"></div>
                                        </div>
                                        <input
                                            className="block w-full rounded-xl border border-[#E3DED1] dark:border-[#3E3C36] bg-white dark:bg-[#262522] py-4 pl-20 pr-4 text-lg text-[#2D332F] dark:text-white placeholder:text-gray-400 focus:border-[#99B898] focus:ring-2 focus:ring-[#99B898]/20 outline-none transition-all duration-200"
                                            id="phone"
                                            placeholder="00000 00000"
                                            type="tel"
                                            value={phone}
                                            onChange={(e) => setPhone(e.target.value.replace(/\D/g, '').slice(0, 10))}
                                        />
                                    </div>
                                </div>
                                <div className="h-2"></div>
                                <button
                                    onClick={handleSendOtp}
                                    className="w-full flex items-center justify-center rounded-xl h-14 px-5 bg-[#99B898] hover:bg-[#84A583] text-[#2D332F] text-lg font-bold tracking-wide shadow-md transition-colors duration-200"
                                >
                                    Send OTP
                                </button>
                                <div className="flex justify-center mt-2">
                                    <button className="text-[#7A8279] dark:text-gray-400 text-base font-medium underline underline-offset-4 hover:text-[#99B898] dark:hover:text-white transition-colors">
                                        Continue as Guest
                                    </button>
                                </div>
                            </div>
                            <div className="flex-1"></div>
                            <div className="text-center pb-2">
                                <p className="text-xs text-[#7A8279] uppercase tracking-widest font-semibold">Secure & Reliable</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="fixed bottom-6 right-6 z-50">
                    <button aria-label="Voice Assistant" className="flex items-center justify-center size-16 rounded-full bg-[#FDFBF7] dark:bg-[#2E2D29] text-[#99B898] shadow-lg border border-[#E3DED1] dark:border-[#3E3C36] hover:scale-105 transition-transform duration-200 group">
                        <span className="material-symbols-outlined text-3xl group-hover:animate-pulse">mic</span>
                        <span className="absolute inline-flex h-full w-full rounded-full bg-[#99B898] opacity-10 animate-ping"></span>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Login;
