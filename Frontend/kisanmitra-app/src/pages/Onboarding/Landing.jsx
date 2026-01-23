import React from 'react';
import { useNavigate } from 'react-router-dom';

const Landing = () => {
    const navigate = useNavigate();

    return (
        <div className="bg-[#fcfbf7] text-[#262626] overflow-x-hidden font-['Space_Grotesk']">
            {/* Header */}
            <header className="fixed top-0 left-0 w-full z-50 bg-[#fcfbf7]/90 backdrop-blur-md border-b border-[#e5e3db]">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center gap-2">
                            <div className="size-8 text-[#608a5c] flex items-center justify-center rounded bg-[#608a5c]/10">
                                <span className="material-symbols-outlined">agriculture</span>
                            </div>
                            <span className="text-[#262626] text-xl font-bold tracking-tight">KisanMitra</span>
                        </div>
                        <div className="hidden md:flex items-center gap-8">
                            <a href="#features" className="text-[#4b5563] hover:text-[#608a5c] text-sm font-medium transition-colors">Features</a>
                            <a href="#how-it-works" className="text-[#4b5563] hover:text-[#608a5c] text-sm font-medium transition-colors">How it Works</a>
                            <a href="#lifecycle" className="text-[#4b5563] hover:text-[#608a5c] text-sm font-medium transition-colors">Lifecycle</a>
                            <a href="#about" className="text-[#4b5563] hover:text-[#608a5c] text-sm font-medium transition-colors">About</a>
                        </div>
                        <div className="flex items-center gap-4">
                            <button onClick={() => navigate('/login')} className="hidden md:flex bg-[#608a5c] hover:bg-[#4a6b47] text-white text-sm font-bold py-2 px-5 rounded-lg transition-colors shadow-sm">
                                Explore Beta
                            </button>
                            <button className="md:hidden text-[#262626]">
                                <span className="material-symbols-outlined">menu</span>
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Hero Section */}
            <section className="relative min-h-[90vh] flex items-center pt-16 overflow-hidden bg-[#fcfbf7]">
                <div className="absolute inset-0 z-0">
                    <div className="absolute inset-0 bg-gradient-to-r from-[#fcfbf7] via-[#fcfbf7]/90 to-[#eaf2eb]/60 z-10"></div>
                    <img
                        alt="Aerial view of lush green farm fields with drone overlay graphic"
                        className="w-full h-full object-cover object-center opacity-40 mix-blend-multiply"
                        src="https://lh3.googleusercontent.com/aida-public/AB6AXuACBhGxD4SdVLUaoSX4N_4ZSw5WmWCS0aESFcWrFTS9JdTPWCBKIF88Uf3xS_chEYU7Y5gmDvgX8TqGCk6hika_3Tje2OVENEM2Gvveb_tjrlpSxNyi1eQCMayJMB-YobvDggnNOgGoHEhhThpfSxYxcL8vfUT-99D0IwSkA1dAXYBXOHqfOsVZI1ykWIFpDd4_qUxDR8mFvJ9kY7qV4uGrgmpIkS_e5xbwCnb-GZp2L84CTGLbROynJO5dxrS00qmz_sG5yX8lyrY"
                    />
                </div>
                <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full py-20">
                    <div className="max-w-3xl">
                        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#608a5c]/10 border border-[#608a5c]/20 text-[#4a6b47] text-xs font-bold uppercase tracking-wider mb-6 shadow-sm">
                            <span className="w-2 h-2 rounded-full bg-[#608a5c] animate-pulse"></span>
                            Live across 5 states
                        </div>
                        <h1 className="text-5xl md:text-7xl font-bold text-[#262626] leading-[1.1] mb-6 tracking-tight">
                            A Voice-First <br />
                            <span className="text-[#608a5c]">Operating System</span> <br />
                            for Indian Farmers
                        </h1>
                        <p className="text-lg md:text-xl text-[#4b5563] mb-10 max-w-xl leading-relaxed font-sans">
                            Bridging the digital divide with an AI-powered copilot that speaks your language. From soil testing to market selling, just ask.
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4">
                            <button onClick={() => navigate('/login')} className="bg-[#608a5c] hover:bg-[#4a6b47] text-white text-base font-bold h-12 px-8 rounded-lg transition-all transform hover:scale-105 flex items-center justify-center gap-2 shadow-md hover:shadow-lg shadow-[#608a5c]/20">
                                Explore Beta
                                <span className="material-symbols-outlined text-lg">arrow_forward</span>
                            </button>
                            <button className="bg-white hover:bg-gray-50 border border-[#e5e3db] text-[#262626] text-base font-bold h-12 px-8 rounded-lg transition-all flex items-center justify-center gap-2 shadow-sm">
                                <span className="material-symbols-outlined text-lg text-[#608a5c]">play_circle</span>
                                Watch Demo
                            </button>
                        </div>
                    </div>
                </div>
                <div className="absolute right-0 bottom-0 md:top-1/2 md:-translate-y-1/2 w-full md:w-1/2 h-[50vh] md:h-full z-0 opacity-10 pointer-events-none">
                    <div className="w-full h-full bg-[url('https://www.transparenttextures.com/patterns/circuit-board.png')] mix-blend-multiply"></div>
                </div>
            </section>

            {/* Challenges Section */}
            <section className="py-24 bg-[#f8f5e4] relative">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="mb-16 md:flex md:items-end md:justify-between">
                        <div className="max-w-2xl">
                            <h2 className="text-3xl md:text-4xl font-bold text-[#262626] mb-4">Challenges in Modern Farming</h2>
                            <p className="text-[#4b5563] text-lg font-sans">Farmers face uncertainty every day. We address the core issues hindering productivity with data, not guesswork.</p>
                        </div>
                        <div className="mt-6 md:mt-0">
                            <a className="text-[#4a6b47] hover:text-[#608a5c] font-bold flex items-center gap-1 transition-colors" href="#">
                                View all challenges <span className="material-symbols-outlined">arrow_right_alt</span>
                            </a>
                        </div>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        <div className="group bg-white border border-[#e8dfc5] hover:border-[#608a5c]/50 p-6 rounded-xl transition-all duration-300 hover:-translate-y-1 shadow-sm hover:shadow-md">
                            <div className="size-12 rounded-lg bg-red-50 text-red-500 flex items-center justify-center mb-4 group-hover:bg-red-100 transition-colors">
                                <span className="material-symbols-outlined text-3xl">visibility_off</span>
                            </div>
                            <h3 className="text-xl font-bold text-[#262626] mb-2">Blind Crop Selection</h3>
                            <p className="text-[#4b5563] text-sm leading-relaxed font-sans">Lack of data-driven insights leads to oversaturated crops and plummeting market prices.</p>
                        </div>
                        <div className="group bg-white border border-[#e8dfc5] hover:border-[#608a5c]/50 p-6 rounded-xl transition-all duration-300 hover:-translate-y-1 shadow-sm hover:shadow-md">
                            <div className="size-12 rounded-lg bg-orange-50 text-orange-500 flex items-center justify-center mb-4 group-hover:bg-orange-100 transition-colors">
                                <span className="material-symbols-outlined text-3xl">thunderstorm</span>
                            </div>
                            <h3 className="text-xl font-bold text-[#262626] mb-2">Weather Uncertainty</h3>
                            <p className="text-[#4b5563] text-sm leading-relaxed font-sans">Unpredictable climate patterns affecting yield without localized micro-weather alerts.</p>
                        </div>
                        <div className="group bg-white border border-[#e8dfc5] hover:border-[#608a5c]/50 p-6 rounded-xl transition-all duration-300 hover:-translate-y-1 shadow-sm hover:shadow-md">
                            <div className="size-12 rounded-lg bg-blue-50 text-blue-500 flex items-center justify-center mb-4 group-hover:bg-blue-100 transition-colors">
                                <span className="material-symbols-outlined text-3xl">storefront</span>
                            </div>
                            <h3 className="text-xl font-bold text-[#262626] mb-2">Market Access Struggle</h3>
                            <p className="text-[#4b5563] text-sm leading-relaxed font-sans">Middlemen eat into profits. Difficulty reaching fair market prices due to lack of connection.</p>
                        </div>
                        <div className="group bg-white border border-[#e8dfc5] hover:border-[#608a5c]/50 p-6 rounded-xl transition-all duration-300 hover:-translate-y-1 shadow-sm hover:shadow-md">
                            <div className="size-12 rounded-lg bg-yellow-50 text-yellow-600 flex items-center justify-center mb-4 group-hover:bg-yellow-100 transition-colors">
                                <span className="material-symbols-outlined text-3xl">pest_control</span>
                            </div>
                            <h3 className="text-xl font-bold text-[#262626] mb-2">Pest Control Gaps</h3>
                            <p className="text-[#4b5563] text-sm leading-relaxed font-sans">Delayed identification of crop diseases results in widespread crop failure.</p>
                        </div>
                        <div className="group bg-white border border-[#e8dfc5] hover:border-[#608a5c]/50 p-6 rounded-xl transition-all duration-300 hover:-translate-y-1 shadow-sm hover:shadow-md">
                            <div className="size-12 rounded-lg bg-amber-50 text-amber-700 flex items-center justify-center mb-4 group-hover:bg-amber-100 transition-colors">
                                <span className="material-symbols-outlined text-3xl">water_drop</span>
                            </div>
                            <h3 className="text-xl font-bold text-[#262626] mb-2">Soil Health Decline</h3>
                            <p className="text-[#4b5563] text-sm leading-relaxed font-sans">Degrading soil quality without proper testing and nutrient management guidance.</p>
                        </div>
                        <div className="group bg-white border border-[#e8dfc5] hover:border-[#608a5c]/50 p-6 rounded-xl transition-all duration-300 hover:-translate-y-1 shadow-sm hover:shadow-md">
                            <div className="size-12 rounded-lg bg-purple-50 text-purple-500 flex items-center justify-center mb-4 group-hover:bg-purple-100 transition-colors">
                                <span className="material-symbols-outlined text-3xl">translate</span>
                            </div>
                            <h3 className="text-xl font-bold text-[#262626] mb-2">Language Barriers</h3>
                            <p className="text-[#4b5563] text-sm leading-relaxed font-sans">Most advanced agri-tech tools are in English, alienating the actual growers.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Solution Section */}
            <section id="features" className="py-24 bg-[#eaf2eb]">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-5xl font-bold text-[#262626] mb-6">The KisanMitra Solution</h2>
                        <p className="text-[#4b5563] text-lg max-w-2xl mx-auto font-sans">An intelligent OS built for the harsh realities of Indian agriculture.</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div className="group overflow-hidden rounded-2xl bg-white border border-[#e5e3db] shadow-lg hover:shadow-xl transition-shadow flex flex-col md:flex-row h-full">
                            <div className="md:w-1/2 relative h-48 md:h-auto">
                                <img alt="Indian farmer talking on a mobile phone in a field" className="absolute inset-0 w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCDW88pkkcwGKEeTGKOYO0RPGpUQYveYistusL4ge2V7p4jwLXL02eItllpi00DxyMVV5daRDSL2iur72H4eJM2uilr4UNZz23nAUOiVtn7BE-2skqaPlovwDq0k4OYMnDAnD9yocgyulYMUpZZpfuCDOsO4JRklsjaomrAnO9e1vrcwIyTz544Ptm-5sGEvBtCyJBIpGiw_3rrrj2KQsyesOLXV4-1QrDlxuMXvyKkpvGvR2GAiSP262D_COCOaljyYAH1VYUHA18" />
                            </div>
                            <div className="md:w-1/2 p-8 flex flex-col justify-center">
                                <div className="bg-[#608a5c]/10 w-fit p-2 rounded-lg mb-4">
                                    <span className="material-symbols-outlined text-[#608a5c] text-3xl">mic</span>
                                </div>
                                <h3 className="text-2xl font-bold text-[#262626] mb-2">Voice-First Interface</h3>
                                <p className="text-[#4b5563] font-sans">Speak naturally in Hindi, Marathi, Tamil, and more. No typing required.</p>
                            </div>
                        </div>
                        <div className="group overflow-hidden rounded-2xl bg-white border border-[#e5e3db] shadow-lg hover:shadow-xl transition-shadow flex flex-col md:flex-row h-full">
                            <div className="md:w-1/2 relative h-48 md:h-auto">
                                <img alt="Abstract AI data visualization overlay on crops" className="absolute inset-0 w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAiqqtVDLqTCYd4503SIzrxcvu5H9GOsS_IVMwzW2AZiiJX_f6Ckcj6FlZx64HIhW45bKHIv6TDZapRrYUpcqEsjqP1WWsauS8861_6N5m3qCoRpK2DbuMIKH8tpLjSxB2JF1RDSY7VFs9q9R0be2i9p5G8F2dy_NuvPQbWF9a2jaCxurzfDEE2FJYHIE5jtcB6OQG42vNL7XPx0v4Mn4m8TFm71RsUAgJBowcdcU4xGnhk_kP_5HUc3H5BGC1MQ04kzymdCnxZWXU" />
                            </div>
                            <div className="md:w-1/2 p-8 flex flex-col justify-center">
                                <div className="bg-[#608a5c]/10 w-fit p-2 rounded-lg mb-4">
                                    <span className="material-symbols-outlined text-[#608a5c] text-3xl">psychology</span>
                                </div>
                                <h3 className="text-2xl font-bold text-[#262626] mb-2">AI Copilot</h3>
                                <p className="text-[#4b5563] font-sans">Real-time decision support engine that analyzes soil, weather, and market data.</p>
                            </div>
                        </div>
                        <div className="group overflow-hidden rounded-2xl bg-white border border-[#e5e3db] shadow-lg hover:shadow-xl transition-shadow flex flex-col md:flex-row h-full">
                            <div className="md:w-1/2 relative h-48 md:h-auto">
                                <img alt="Stages of plant growth from seedling to harvest" className="absolute inset-0 w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCrLdxO7Hjxct8h_tvG3XpcH7yeMj6BePyN6lqAcm4Q1q3j59UArwha2G0MJ2B_SqPN2oOQnEhHaiWVa1UMGIdX1JTQ71ULg0Bo-1D5K3kEXAoO4bc-rnuj6rsa83WELN04J8EePKqpCWYdQzmm3x_dOHWVTv5LW6c80IrL2eVJ9GoAcRIhCg4zCsB_YURYIrdUWcRnIqeIhmeEzXSHUOWdGPxItGLO2TK39PqWp2YOewJah-jqdiXAE9qrovGou35Znht5nJ6RVBc" />
                            </div>
                            <div className="md:w-1/2 p-8 flex flex-col justify-center">
                                <div className="bg-[#608a5c]/10 w-fit p-2 rounded-lg mb-4">
                                    <span className="material-symbols-outlined text-[#608a5c] text-3xl">cycle</span>
                                </div>
                                <h3 className="text-2xl font-bold text-[#262626] mb-2">Lifecycle-Based</h3>
                                <p className="text-[#4b5563] font-sans">Comprehensive support from seed selection to post-harvest selling.</p>
                            </div>
                        </div>
                        <div className="group overflow-hidden rounded-2xl bg-white border border-[#e5e3db] shadow-lg hover:shadow-xl transition-shadow flex flex-col md:flex-row h-full">
                            <div className="md:w-1/2 relative h-48 md:h-auto">
                                <img alt="Rural area with minimal infrastructure" className="absolute inset-0 w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCaumYUw8AhNubXKG4KTTOqSljsVbKvbrOFXjF4HrNCKG2MmXqyNTBhnV4jF6WqDmORc9W26pjj42P1HwSES7TnFvGtjN-lTVDd_fh-lw_ybBG5Xi3zugDdLH-3GvhUS-hJnbC6164cWDt_jZa1HFJrM4XeaUiPP5dhN9GMTIdYl-0tfWksGyuGj-S9qTqEmQvGBDFueH7ClDabhnYOIEnGzM_j3uI2vvKtxI0gGFYcukpejdi0r5KjVQtlm3AbFJynD3JlXSakmUw" />
                            </div>
                            <div className="md:w-1/2 p-8 flex flex-col justify-center">
                                <div className="bg-[#608a5c]/10 w-fit p-2 rounded-lg mb-4">
                                    <span className="material-symbols-outlined text-[#608a5c] text-3xl">signal_cellular_alt</span>
                                </div>
                                <h3 className="text-2xl font-bold text-[#262626] mb-2">Built for Real Farmers</h3>
                                <p className="text-[#4b5563] font-sans">Works seamlessly on low bandwidth 2G/3G networks and basic smartphones.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section id="how-it-works" className="py-24 bg-white border-y border-[#e5e3db]">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold text-[#262626]">How It Works</h2>
                    </div>
                    <div className="relative grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div className="hidden md:block absolute top-12 left-[16%] right-[16%] h-0.5 border-t-2 border-dashed border-gray-300 z-0"></div>
                        <div className="relative z-10 flex flex-col items-center text-center">
                            <div className="size-24 rounded-full bg-[#fcfbf7] border-4 border-white ring-2 ring-[#608a5c]/30 flex items-center justify-center mb-6 shadow-lg">
                                <span className="material-symbols-outlined text-[#608a5c] text-4xl">app_registration</span>
                            </div>
                            <div className="bg-[#fcfbf7] border border-[#e5e3db] p-6 rounded-xl w-full hover:border-[#608a5c]/30 transition-colors shadow-sm">
                                <h3 className="text-xl font-bold text-[#262626] mb-2">1. Quick Setup</h3>
                                <p className="text-[#4b5563] text-sm font-sans">Download the app and create a profile with your location and farm size.</p>
                            </div>
                        </div>
                        <div className="relative z-10 flex flex-col items-center text-center">
                            <div className="size-24 rounded-full bg-[#fcfbf7] border-4 border-white ring-2 ring-[#608a5c]/30 flex items-center justify-center mb-6 shadow-lg">
                                <span className="material-symbols-outlined text-[#608a5c] text-4xl">graphic_eq</span>
                            </div>
                            <div className="bg-[#fcfbf7] border border-[#e5e3db] p-6 rounded-xl w-full hover:border-[#608a5c]/30 transition-colors shadow-sm">
                                <h3 className="text-xl font-bold text-[#262626] mb-2">2. Just Talk</h3>
                                <p className="text-[#4b5563] text-sm font-sans">Press the mic button and ask any question about your crops in your language.</p>
                            </div>
                        </div>
                        <div className="relative z-10 flex flex-col items-center text-center">
                            <div className="size-24 rounded-full bg-[#fcfbf7] border-4 border-white ring-2 ring-[#608a5c]/30 flex items-center justify-center mb-6 shadow-lg">
                                <span className="material-symbols-outlined text-[#608a5c] text-4xl">analytics</span>
                            </div>
                            <div className="bg-[#fcfbf7] border border-[#e5e3db] p-6 rounded-xl w-full hover:border-[#608a5c]/30 transition-colors shadow-sm">
                                <h3 className="text-xl font-bold text-[#262626] mb-2">3. Get Insights</h3>
                                <p className="text-[#4b5563] text-sm font-sans">Receive actionable advice, weather alerts, and market prices instantly.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Lifecycle Support Section */}
            <section id="lifecycle" className="py-24 bg-[#fcfbf7]">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <h2 className="text-3xl md:text-4xl font-bold text-[#262626] mb-12">Complete Farm Lifecycle Support</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="bg-[#dce6dd] p-8 rounded-2xl border border-[#608a5c]/10 shadow-sm">
                            <div className="flex items-center gap-4 mb-8">
                                <div className="p-3 bg-white rounded-lg text-[#608a5c] shadow-sm">
                                    <span className="material-symbols-outlined text-2xl">potted_plant</span>
                                </div>
                                <h3 className="text-2xl font-bold text-[#262626]">Pre-Seeding</h3>
                            </div>
                            <ul className="space-y-4">
                                <li className="flex items-start gap-3 text-[#4b5563] font-sans">
                                    <span className="material-symbols-outlined text-[#4a6b47] text-lg mt-0.5">check_circle</span>
                                    <span>Soil testing analysis via AI vision</span>
                                </li>
                                <li className="flex items-start gap-3 text-[#4b5563] font-sans">
                                    <span className="material-symbols-outlined text-[#4a6b47] text-lg mt-0.5">check_circle</span>
                                    <span>Optimal crop selection advice</span>
                                </li>
                                <li className="flex items-start gap-3 text-[#4b5563] font-sans">
                                    <span className="material-symbols-outlined text-[#4a6b47] text-lg mt-0.5">check_circle</span>
                                    <span>Seed procurement planning</span>
                                </li>
                            </ul>
                        </div>
                        <div className="bg-[#f5ebd0] p-8 rounded-2xl border border-[#dcb758]/30 shadow-md relative overflow-hidden">
                            <div className="absolute top-0 left-0 w-full h-1 bg-[#dcb758]"></div>
                            <div className="flex items-center gap-4 mb-8">
                                <div className="p-3 bg-[#dcb758] text-white rounded-lg shadow-sm">
                                    <span className="material-symbols-outlined text-2xl">agriculture</span>
                                </div>
                                <h3 className="text-2xl font-bold text-[#262626]">While Farming</h3>
                            </div>
                            <ul className="space-y-4">
                                <li className="flex items-start gap-3 text-[#4b5563] font-sans">
                                    <span className="material-symbols-outlined text-yellow-700 text-lg mt-0.5">check_circle</span>
                                    <span>Real-time disease detection</span>
                                </li>
                                <li className="flex items-start gap-3 text-[#4b5563] font-sans">
                                    <span className="material-symbols-outlined text-yellow-700 text-lg mt-0.5">check_circle</span>
                                    <span>Micro-weather alerts & irrigation</span>
                                </li>
                                <li className="flex items-start gap-3 text-[#4b5563] font-sans">
                                    <span className="material-symbols-outlined text-yellow-700 text-lg mt-0.5">check_circle</span>
                                    <span>Fertilizer dosage calculator</span>
                                </li>
                            </ul>
                        </div>
                        <div className="bg-[#dce6dd] p-8 rounded-2xl border border-[#608a5c]/10 shadow-sm">
                            <div className="flex items-center gap-4 mb-8">
                                <div className="p-3 bg-white rounded-lg text-[#608a5c] shadow-sm">
                                    <span className="material-symbols-outlined text-2xl">local_shipping</span>
                                </div>
                                <h3 className="text-2xl font-bold text-[#262626]">Post-Harvest</h3>
                            </div>
                            <ul className="space-y-4">
                                <li className="flex items-start gap-3 text-[#4b5563] font-sans">
                                    <span className="material-symbols-outlined text-[#4a6b47] text-lg mt-0.5">check_circle</span>
                                    <span>Live Mandi (Market) prices</span>
                                </li>
                                <li className="flex items-start gap-3 text-[#4b5563] font-sans">
                                    <span className="material-symbols-outlined text-[#4a6b47] text-lg mt-0.5">check_circle</span>
                                    <span>Storage availability finder</span>
                                </li>
                                <li className="flex items-start gap-3 text-[#4b5563] font-sans">
                                    <span className="material-symbols-outlined text-[#4a6b47] text-lg mt-0.5">check_circle</span>
                                    <span>Transport logistics support</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </section>

            {/* Differentiation Section */}
            <section id="about" className="py-24 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <h2 className="text-3xl font-bold text-[#262626] mb-10 border-b border-[#e5e3db] pb-6">What Makes KisanMitra Different?</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="bg-[#fcfbf7] p-8 border border-[#e5e3db] rounded-lg hover:border-[#608a5c]/40 transition-colors">
                            <h3 className="text-xl font-bold text-[#262626] mb-2 flex items-center gap-2">
                                <span className="material-symbols-outlined text-[#608a5c]">smart_toy</span> Agentic AI
                            </h3>
                            <p className="text-[#4b5563] font-sans">Not just a chatbot. It takes actions on your behalf, like scheduling reminders or calculating costs.</p>
                        </div>
                        <div className="bg-[#fcfbf7] p-8 border border-[#e5e3db] rounded-lg hover:border-[#608a5c]/40 transition-colors">
                            <h3 className="text-xl font-bold text-[#262626] mb-2 flex items-center gap-2">
                                <span className="material-symbols-outlined text-[#608a5c]">language</span> 12+ Local Languages
                            </h3>
                            <p className="text-[#4b5563] font-sans">Built with deep dialect understanding for rural India, not just Google Translate.</p>
                        </div>
                        <div className="bg-[#fcfbf7] p-8 border border-[#e5e3db] rounded-lg hover:border-[#608a5c]/40 transition-colors">
                            <h3 className="text-xl font-bold text-[#262626] mb-2 flex items-center gap-2">
                                <span className="material-symbols-outlined text-[#608a5c]">offline_bolt</span> Offline Capable
                            </h3>
                            <p className="text-[#4b5563] font-sans">Core features work without internet. Syncs when you are back online.</p>
                        </div>
                        <div className="bg-[#fcfbf7] p-8 border border-[#e5e3db] rounded-lg hover:border-[#608a5c]/40 transition-colors">
                            <h3 className="text-xl font-bold text-[#262626] mb-2 flex items-center gap-2">
                                <span className="material-symbols-outlined text-[#608a5c]">verified_user</span> Trust-First
                            </h3>
                            <p className="text-[#4b5563] font-sans">Data privacy is paramount. Your farm data is yours, encrypted and secure.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="relative py-32 overflow-hidden bg-[#caddc7]">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-white/30 to-transparent opacity-60"></div>
                <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
                    <h2 className="text-4xl md:text-6xl font-black text-[#262626] mb-6 tracking-tight">
                        Farming should not <br /> be confusing.
                    </h2>
                    <p className="text-xl text-[#262626]/80 mb-10 font-sans">
                        Join 50,000+ farmers modernizing their yield with KisanMitra.
                    </p>
                    <div className="flex flex-col sm:flex-row justify-center gap-4">
                        <button onClick={() => navigate('/login')} className="bg-[#262626] hover:bg-black text-white text-lg font-bold py-4 px-10 rounded-full transition-all transform hover:scale-105 shadow-xl shadow-black/10">
                            Join Waitlist
                        </button>
                        <button className="bg-transparent border-2 border-[#262626] hover:bg-white/20 text-[#262626] text-lg font-bold py-4 px-10 rounded-full transition-all">
                            View Interactive Demo
                        </button>
                    </div>
                    <p className="mt-8 text-sm text-[#262626]/60">© 2024 KisanMitra. Built for Bharat.</p>
                </div>
            </section>
        </div>
    );
};

export default Landing;
