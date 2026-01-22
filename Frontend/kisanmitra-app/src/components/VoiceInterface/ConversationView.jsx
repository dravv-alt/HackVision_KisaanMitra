import React, { useEffect, useRef } from 'react';
import { Mic } from 'lucide-react';
import CropCard from './cards/CropCard';
import MarketPriceCard from './cards/MarketPriceCard';
import SchemeCard from './cards/SchemeCard';
import ConfirmationCard from './cards/ConfirmationCard';
import FinanceCard from './cards/FinanceCard';
import ContextIndicator from './ContextIndicator';
import AudioPlayer from './AudioPlayer';
import TranscriptBox from './TranscriptBox';

const ConversationView = ({ messages, onMicClick }) => {
    const chatEndRef = useRef(null);

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const renderCard = (cardData) => {
        if (!cardData) return null;
        switch (cardData.type) {
            case 'cropRecommendation':
                return <CropCard {...cardData.data} />;
            case 'marketPrice':
                return <MarketPriceCard {...cardData.data} />;
            case 'governmentScheme':
                return <SchemeCard {...cardData.data} />;
            case 'financialInsight':
                return <FinanceCard {...cardData.data} />;
            case 'confirmation':
                return <ConfirmationCard {...cardData.data} />;
            default:
                return null;
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>

            {/* Chat Area - Flexible Height */}
            <div className="chat-area">
                {messages.length === 0 && (
                    <div style={{ textAlign: 'center', color: 'var(--text-secondary)', marginTop: '40px' }}>
                        Start speaking to see conversation here...
                    </div>
                )}

                {messages.map((msg, idx) => (
                    <div key={idx} style={{ marginBottom: '24px' }}>

                        {/* Context Indicator (if present, usually for AI msgs) */}
                        {msg.context && (
                            <div style={{ display: 'flex', justifyContent: 'flex-start', marginBottom: '8px' }}>
                                <ContextIndicator contextItems={msg.context} />
                            </div>
                        )}

                        <div className={`message-bubble ${msg.type === 'user' ? 'message-user' : 'message-ai'}`}>

                            {/* Text Content */}
                            {msg.text && <div style={{ marginBottom: (msg.cardData || msg.audio) ? '12px' : '0' }}>{msg.text}</div>}

                            {/* Render Card if present */}
                            {msg.cardData && renderCard(msg.cardData)}

                            {/* Audio Player & Transcript (for AI) */}
                            {msg.type === 'ai' && (
                                <>
                                    {msg.audio && <AudioPlayer duration={msg.audio.duration} transcript={msg.audio.transcript} />}
                                    {msg.transcript && <TranscriptBox text={msg.transcript} />}
                                </>
                            )}

                            {/* Timestamp */}
                            <div style={{
                                marginTop: '8px',
                                fontSize: '0.7rem',
                                color: 'var(--text-secondary)',
                                textAlign: msg.type === 'user' ? 'right' : 'left',
                                opacity: 0.7
                            }}>
                                {msg.timestamp}
                            </div>
                        </div>
                    </div>
                ))}
                <div ref={chatEndRef} />
            </div>

            {/* Input Bar - Fixed Bottom */}
            <div className="input-bar">
                <input
                    type="text"
                    placeholder="Type or speak..."
                    className="text-input"
                />
                <button className="mic-btn-small" onClick={onMicClick}>
                    <Mic size={24} />
                </button>
            </div>
        </div>
    );
};

export default ConversationView;
