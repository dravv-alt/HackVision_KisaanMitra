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

                console.log('✅ Token stored, redirecting...');

                // Navigate based on onboarding status
                setTimeout(() => {
                    if (data.needs_onboarding) {
                        navigate('/onboarding/language');
                    } else {
                        navigate('/dashboard');
                    }
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
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-green-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center px-4 py-8">
            <div className="max-w-md w-full">
                {/* Logo and Title */}
                <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 bg-green-600 rounded-full mb-4">
                        <span className="material-symbols-outlined text-white text-4xl">agriculture</span>
                    </div>
                    <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                        किसानमित्र
                    </h1>
                    <p className="text-gray-600 dark:text-gray-400">
                        {step === 'phone' ? 'अपने फ़ोन नंबर से लॉगिन करें' : 'OTP दर्ज करें'}
                    </p>
                </div>

                {/* Login Card */}
                <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
                    {/* Debug Info */}
                    {debugInfo && (
                        <div className="mb-4 p-4 bg-yellow-100 border border-yellow-400 text-yellow-800 rounded-lg text-sm">
                            <strong>Debug:</strong> {debugInfo}
                        </div>
                    )}

                    {/* Success Message */}
                    {success && (
                        <div className="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
                            ✅ {success}
                        </div>
                    )}

                    {/* Error Message */}
                    {error && (
                        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
                            ❌ {error}
                        </div>
                    )}

                    {step === 'phone' ? (
                        <form onSubmit={handleSendOTP}>
                            <div className="mb-6">
                                <label className="block text-gray-700 dark:text-gray-300 text-sm font-semibold mb-2">
                                    फ़ोन नंबर (Phone Number)
                                </label>
                                <div className="flex">
                                    <span className="inline-flex items-center px-4 bg-gray-100 dark:bg-gray-700 border border-r-0 border-gray-300 dark:border-gray-600 rounded-l-lg text-gray-700 dark:text-gray-300">
                                        +91
                                    </span>
                                    <input
                                        type="tel"
                                        value={phoneNumber}
                                        onChange={(e) => setPhoneNumber(e.target.value)}
                                        placeholder="9876543210"
                                        className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-r-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:text-white"
                                        required
                                        pattern="[0-9]{10}"
                                        maxLength="10"
                                    />
                                </div>
                                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                                    आपको OTP SMS के माध्यम से भेजा जाएगा
                                </p>
                            </div>

                            <button
                                type="submit"
                                disabled={loading || phoneNumber.length !== 10}
                                className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2"
                            >
                                {loading ? (
                                    <>
                                        <span className="animate-spin material-symbols-outlined">progress_activity</span>
                                        <span>भेजा जा रहा है...</span>
                                    </>
                                ) : (
                                    <>
                                        <span>OTP भेजें</span>
                                        <span className="material-symbols-outlined">arrow_forward</span>
                                    </>
                                )}
                            </button>
                        </form>
                    ) : (
                        <form onSubmit={handleVerifyOTP}>
                            <div className="mb-6">
                                <label className="block text-gray-700 dark:text-gray-300 text-sm font-semibold mb-2">
                                    OTP दर्ज करें (Enter OTP)
                                </label>
                                <input
                                    type="text"
                                    value={otp}
                                    onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                                    placeholder="123456"
                                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 dark:bg-gray-700 dark:text-white text-center text-2xl tracking-widest"
                                    required
                                    maxLength="6"
                                    autoFocus
                                />
                                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400 text-center">
                                    +91 {phoneNumber} पर भेजा गया
                                </p>
                                <p className="mt-1 text-sm text-green-600 dark:text-green-400 text-center">
                                    OTP {expiresIn} मिनट के लिए मान्य है
                                </p>
                            </div>

                            <button
                                type="submit"
                                disabled={loading || otp.length !== 6}
                                className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center gap-2 mb-4"
                            >
                                {loading ? (
                                    <>
                                        <span className="animate-spin material-symbols-outlined">progress_activity</span>
                                        <span>सत्यापित किया जा रहा है...</span>
                                    </>
                                ) : (
                                    <>
                                        <span>सत्यापित करें और लॉगिन करें</span>
                                        <span className="material-symbols-outlined">check_circle</span>
                                    </>
                                )}
                            </button>

                            <div className="flex items-center justify-between">
                                <button
                                    type="button"
                                    onClick={() => {
                                        setStep('phone');
                                        setOtp('');
                                        setError('');
                                        setSuccess('');
                                        setDebugInfo('');
                                    }}
                                    className="text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 text-sm"
                                >
                                    ← नंबर बदलें
                                </button>
                                <button
                                    type="button"
                                    onClick={handleResendOTP}
                                    disabled={loading}
                                    className="text-green-600 dark:text-green-400 hover:text-green-800 dark:hover:text-green-200 text-sm font-semibold"
                                >
                                    OTP फिर से भेजें
                                </button>
                            </div>
                        </form>
                    )}
                </div>

                {/* Footer */}
                <p className="text-center text-gray-600 dark:text-gray-400 text-sm mt-6">
                    लॉगिन करके, आप हमारी सेवा की शर्तों से सहमत हैं
                </p>

                {/* Debug Panel */}
                <div className="mt-4 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg text-xs">
                    <p className="font-semibold mb-2">Debug Info:</p>
                    <p>Step: {step}</p>
                    <p>Phone: {phoneNumber ? formatPhoneNumber(phoneNumber) : 'Not entered'}</p>
                    <p>OTP Length: {otp.length}/6</p>
                    <p>Backend: http://localhost:8000</p>
                </div>
            </div>
        </div>
    );
};

export default Login;
