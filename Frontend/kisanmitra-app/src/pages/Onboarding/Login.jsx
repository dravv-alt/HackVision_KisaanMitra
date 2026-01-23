import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const navigate = useNavigate();

    const [step, setStep] = useState('phone'); // 'phone' or 'otp'
    const [phoneNumber, setPhoneNumber] = useState('');
    const [otp, setOtp] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [expiresIn, setExpiresIn] = useState(10);
    const [debugInfo, setDebugInfo] = useState('');

    const formatPhoneNumber = (phone) => {
        // Remove all non-digits
        const digits = phone.replace(/\D/g, '');

        // If starts with 91, keep it, otherwise add +91
        if (digits.startsWith('91')) {
            return '+' + digits;
        } else if (digits.length === 10) {
            return '+91' + digits;
        }
        return '+' + digits;
    };

    const handleSendOTP = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setDebugInfo('');
        setLoading(true);

        try {
            const formattedPhone = formatPhoneNumber(phoneNumber);
            console.log('📱 Sending OTP to:', formattedPhone);

            const response = await fetch('http://localhost:8000/api/v1/auth/send-otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    phone_number: formattedPhone
                }),
            });

            const data = await response.json();
            console.log('📨 Response:', data);

            if (response.ok) {
                setSuccess('OTP sent successfully!');
                console.log('🔄 Switching to OTP step...');
                setStep('otp');
                setExpiresIn(data.expires_in_minutes || 10);

                // Show OTP in console and alert for development (mock mode)
                if (data.otp) {
                    console.log('🔐 Development OTP:', data.otp);
                    setDebugInfo(`Development Mode - OTP: ${data.otp}`);
                    alert(`Development Mode: Your OTP is ${data.otp}`);
                }
            } else {
                console.error('❌ Server returned error:', data);
                setError(data.detail || data.message || 'Failed to send OTP');
            }
        } catch (err) {
            console.error('❌ Network error exception:', err);
            setError(`Network error: ${err.message}. Ensure backend is running.`);
        } finally {
            setLoading(false);
        }
    };

    const handleVerifyOTP = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        setLoading(true);

        try {
            const formattedPhone = formatPhoneNumber(phoneNumber);
            console.log('🔐 Verifying OTP:', otp, 'for phone:', formattedPhone);

            const response = await fetch('http://localhost:8000/api/v1/auth/verify-otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    phone_number: formattedPhone,
                    otp: otp
                }),
            });

            const data = await response.json();
            console.log('✅ Verification response:', data);

            if (response.ok) {
                setSuccess('Login successful!');

                // Store auth token
                localStorage.setItem('kisanmitra_auth_token', data.access_token);
                localStorage.setItem('kisanmitra_user_id', data.user_id);
                localStorage.setItem('kisanmitra_farmer_id', data.farmer_id);

                // RESET onboarding status to ensure user sees the onboarding flow (as requested)
                localStorage.removeItem('kisanmitra_onboarding_completed');

                console.log('✅ Token stored, redirecting to Onboarding...');

                // Always navigate to onboarding for this flow
                setTimeout(() => {
                    navigate('/onboarding/language');
                }, 1000);
            } else {
                setError(data.detail || data.message || 'Invalid OTP');
                console.error('❌ Verification failed:', data);
            }
        } catch (err) {
            setError(`Network error: ${err.message}`);
            console.error('❌ Network error:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleResendOTP = async () => {
        setError('');
        setSuccess('');
        setDebugInfo('');
        setLoading(true);

        try {
            const formattedPhone = formatPhoneNumber(phoneNumber);

            const response = await fetch('http://localhost:8000/api/v1/auth/resend-otp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    phone_number: formattedPhone
                }),
            });

            const data = await response.json();

            if (response.ok) {
                setOtp('');
                setSuccess('OTP resent successfully!');
                setExpiresIn(data.expires_in_minutes || 10);

                // Show OTP in console for development
                if (data.otp) {
                    console.log('🔐 Development OTP:', data.otp);
                    setDebugInfo(`Development Mode - OTP: ${data.otp}`);
                    alert(`Development Mode: Your OTP is ${data.otp}`);
                }
            } else {
                setError(data.detail || 'Failed to resend OTP');
            }
        } catch (err) {
            setError('Network error. Please try again.');
        } finally {
            setLoading(false);
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

                            {/* Debug Info */}
                            {debugInfo && (
                                <div className="p-3 bg-yellow-100 border border-yellow-400 text-yellow-800 rounded-lg text-sm text-center">
                                    <strong>Debug:</strong> {debugInfo}
                                </div>
                            )}

                            {/* Success Message */}
                            {success && (
                                <div className="p-3 bg-green-100 border border-green-400 text-green-700 rounded-lg text-center">
                                    ✅ {success}
                                </div>
                            )}

                            {/* Error Message */}
                            {error && (
                                <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg text-center">
                                    ❌ {error}
                                </div>
                            )}

                            {step === 'phone' ? (
                                <form onSubmit={handleSendOTP} className="flex flex-col gap-6 mt-4">
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
                                                value={phoneNumber}
                                                onChange={(e) => setPhoneNumber(e.target.value.replace(/\D/g, '').slice(0, 10))}
                                                required
                                                pattern="[0-9]{10}"
                                                maxLength="10"
                                            />
                                        </div>
                                    </div>
                                    
                                    <div className="h-2"></div>
                                    
                                    <button
                                        type="submit"
                                        disabled={loading || phoneNumber.length !== 10}
                                        className="w-full flex items-center justify-center rounded-xl h-14 px-5 bg-[#99B898] hover:bg-[#84A583] disabled:bg-gray-400 disabled:cursor-not-allowed text-[#2D332F] text-lg font-bold tracking-wide shadow-md transition-colors duration-200 gap-2"
                                    >
                                        {loading ? (
                                            <>
                                                <span className="animate-spin material-symbols-outlined">progress_activity</span>
                                                <span>Sending...</span>
                                            </>
                                        ) : (
                                            'Send OTP'
                                        )}
                                    </button>
                                    
                                    <div className="flex justify-center mt-2">
                                        <button 
                                            type="button"
                                            className="text-[#7A8279] dark:text-gray-400 text-base font-medium underline underline-offset-4 hover:text-[#99B898] dark:hover:text-white transition-colors"
                                        >
                                            Continue as Guest
                                        </button>
                                    </div>
                                </form>
                            ) : (
                                <form onSubmit={handleVerifyOTP} className="flex flex-col gap-6 mt-4">
                                    <div className="flex flex-col gap-2">
                                        <label className="text-[#2D332F] dark:text-gray-200 text-base font-semibold ml-1">
                                            Enter the OTP sent to +91 {phoneNumber}
                                        </label>
                                        <input
                                            type="text"
                                            value={otp}
                                            onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                                            placeholder="123456"
                                            className="block w-full rounded-xl border border-[#E3DED1] dark:border-[#3E3C36] bg-white dark:bg-[#262522] py-4 px-4 text-center text-2xl tracking-[0.5em] text-[#2D332F] dark:text-white placeholder:text-gray-400 focus:border-[#99B898] focus:ring-2 focus:ring-[#99B898]/20 outline-none transition-all duration-200"
                                            required
                                            maxLength="6"
                                            autoFocus
                                        />
                                        <p className="text-center text-sm text-[#99B898] mt-1">
                                            Valid for {expiresIn} minutes
                                        </p>
                                    </div>

                                    <div className="h-2"></div>

                                    <button
                                        type="submit"
                                        disabled={loading || otp.length !== 6}
                                        className="w-full flex items-center justify-center rounded-xl h-14 px-5 bg-[#99B898] hover:bg-[#84A583] disabled:bg-gray-400 disabled:cursor-not-allowed text-[#2D332F] text-lg font-bold tracking-wide shadow-md transition-colors duration-200 gap-2"
                                    >
                                        {loading ? (
                                            <>
                                                <span className="animate-spin material-symbols-outlined">progress_activity</span>
                                                <span>Verifying...</span>
                                            </>
                                        ) : (
                                            <>
                                                <span>Verify & Login</span>
                                                <span className="material-symbols-outlined">check_circle</span>
                                            </>
                                        )}
                                    </button>

                                    <div className="flex justify-between items-center px-2">
                                        <button
                                            type="button"
                                            onClick={() => {
                                                setStep('phone');
                                                setOtp('');
                                                setError('');
                                                setSuccess('');
                                            }}
                                            className="text-[#7A8279] dark:text-gray-400 hover:text-[#99B898] text-sm font-medium"
                                        >
                                            ← Change Number
                                        </button>
                                        <button
                                            type="button"
                                            onClick={handleResendOTP}
                                            disabled={loading}
                                            className="text-[#99B898] hover:text-[#84A583] text-sm font-bold"
                                        >
                                            Resend OTP
                                        </button>
                                    </div>
                                </form>
                            )}

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

