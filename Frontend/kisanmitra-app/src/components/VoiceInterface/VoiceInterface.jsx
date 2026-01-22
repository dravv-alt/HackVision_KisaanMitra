import React, { useState, useEffect } from 'react';
import { Mic, X, MoreHorizontal, User } from 'lucide-react';
import './styles/voice-interface.css';
import IdleHome from './IdleHome';
import ListeningState from './ListeningState';
import ConversationView from './ConversationView';

// Sample Context for demo
const DEMO_CONTEXT = {
    location: 'Pune, MH',
    crop: 'Wheat',
    soil: 'Black Soil'
};

const VoiceInterface = ({ isOpen, onClose }) => {
    const [viewState, setViewState] = useState('idle'); // idle, listening, conversation
    const [messages, setMessages] = useState([]);

    // Reset state when opened
    useEffect(() => {
        if (isOpen) {
            setViewState('idle');
            setMessages([]);
        }
    }, [isOpen]);

    const startListening = () => {
        setViewState('listening');
        // Simulate listening delay then go to conversation
        setTimeout(() => {
            handleDemoConversation();
        }, 2000);
    };

    const cancelListening = () => {
        setViewState('idle');
    };

    // Orchestrates a demo conversation flow
    const handleDemoConversation = () => {
        setViewState('conversation');

        // Step 1: User asks about price
        addMessage('user', "Mandi mein Gehu ka kya bhav hai? (What is wheat price?)");

        // Step 2: AI Response with Market Price Card
        setTimeout(() => {
            addMessage('ai', "Pune mandi mein aaj ka updated bhav ₹2,850 hai.", {
                type: 'marketPrice',
                data: {
                    crop: 'Wheat (Sharbati)',
                    price: '₹2,850',
                    trend: 'Rising',
                    trendValue: '+2.4%',
                    trendDir: 'up',
                    lastUpdated: '2 hours ago'
                }
            }, {
                duration: 8,
                transcript: "Pune mandi mein aaj ka updated bhav ₹2,850 hai. Ye pichle hafte se thoda badha hai."
            }, ['Location: Pune', 'Crop: Wheat']);

            // Step 3: User asks about schemes (Auto-trigger for demo)
            setTimeout(() => {
                addMessage('user', "Kya iske liye koi scheme hai?");

                // Step 4: AI Response with Scheme Card
                // Step 4: AI Response with Scheme Card
                setTimeout(() => {
                    addMessage('ai', "Ji haan, Pradhan Mantri Fasal Bima Yojana available hai.", {
                        type: 'governmentScheme',
                        data: {
                            title: 'Pradhan Mantri Fasal Bima Yojana',
                            isTopRecommendation: true,
                            benefitAmount: 'Up to ₹50,000/ha',
                            description: 'This scheme provides comprehensive insurance coverage to farmers against failure of crops due to non-preventable natural risks, pests, and diseases. It aims to stabilize farmer income and ensure credit flow.'
                        }
                    }, {
                        duration: 6,
                        transcript: "Ji haan, Pradhan Mantri Fasal Bima Yojana available hai. Isme aapko ₹50,000 tak ka insurance mil sakta hai."
                    });

                    // Step 5: Agentic Action (Tractor)
                    setTimeout(() => {
                        addMessage('ai', "Kya main local dealer se tractor rental ke liye baat kar lun?", {
                            type: 'confirmation',
                            data: {
                                question: "Main tractor rental ke liye apply kar doon?",
                                details: [
                                    { icon: '🚜', text: 'Mahindra 575' },
                                    { icon: '💰', text: '₹800 per day' },
                                    { icon: '📅', text: 'Available: Tomorrow' }
                                ],
                                onConfirm: () => alert('Action Confirmed!'),
                                onCancel: () => alert('Action Cancelled')
                            }
                        }, {
                            duration: 4,
                            transcript: "Kya main local dealer se tractor rental ke liye baat kar lun? Kal subah available hai."
                        });
                    }, 5000);

                    // Step 6: Finance Query
                    setTimeout(() => {
                        addMessage('user', "Pichle mahine ka kharcha kitna hua?");

                        setTimeout(() => {
                            addMessage('ai', "October mahine mein kul kharcha ₹14,250 tha.", {
                                type: 'financialInsight',
                                data: {
                                    month: 'October',
                                    totalExpense: '₹14,250',
                                    categories: [
                                        { name: 'Fertilizers', amount: '₹5,400' },
                                        { name: 'Labor', amount: '₹4,000' },
                                        { name: 'Seeds', amount: '₹3,200' }
                                    ]
                                }
                            }, {
                                duration: 5,
                                transcript: "October mahine mein kul kharcha ₹14,250 tha. Sabse zyada kharcha fertilizers aur labor par hua."
                            });
                        }, 1500);

                    }, 12000); // Extended delay after tractor step

                }, 1500);

            }, 4000);

        }, 1500);
    };

    const addMessage = (type, text, cardData = null, audio = null, context = null) => {
        setMessages(prev => [...prev, {
            type,
            text,
            cardData,
            audio,
            transcript: audio?.transcript, // For text transcript box
            context,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }]);
    };

    if (!isOpen) return null;

    return (
        <div className="voice-interface-overlay" onClick={(e) => {
            // Close if clicked outside container
            if (e.target.className === 'voice-interface-overlay') onClose();
        }}>
            <div className="voice-interface-container" onClick={e => e.stopPropagation()}>
                {/* Top Bar */}
                <div className="top-bar">
                    <button onClick={onClose} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
                        <X size={24} color="var(--text-primary)" />
                    </button>
                    <span style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>KisanMitra</span>
                    <div style={{ width: '32px', height: '32px', borderRadius: '50%', backgroundColor: '#ddd', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <User size={18} />
                    </div>
                </div>

                {/* Content Area */}
                {viewState === 'idle' && (
                    <IdleHome onMicClick={startListening} />
                )}

                {viewState === 'listening' && (
                    <ListeningState onCancel={cancelListening} />
                )}

                {viewState === 'conversation' && (
                    <ConversationView messages={messages} onMicClick={startListening} />
                )}
            </div>
        </div>
    );
};

export default VoiceInterface;
