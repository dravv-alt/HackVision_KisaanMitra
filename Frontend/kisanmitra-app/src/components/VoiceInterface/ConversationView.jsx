import React, { useEffect, useRef } from 'react';
import { Mic, Send, Square } from 'lucide-react';
import CropCard from './cards/CropCard';
import MarketPriceCard from './cards/MarketPriceCard';
import SchemeCard from './cards/SchemeCard';
import ConfirmationCard from './cards/ConfirmationCard';
import FinanceCard from './cards/FinanceCard';
import ContextIndicator from './ContextIndicator';
import AudioPlayer from './AudioPlayer';
import TranscriptBox from './TranscriptBox';

const ConversationView = ({
    messages,
    onMicClick,
    inputText,
    onInputChange,
    onSubmit,
    isLoading,
    isRecording
}) => {
    const chatEndRef = useRef(null);

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            onSubmit(inputText);
        }
    };

    const handleSendClick = () => {
        onSubmit(inputText);
    };

    const renderCard = (cardData) => {
        if (!cardData) return null;

        // Extract data for easier access
        const data = cardData.data || {};

        switch (cardData.type) {
            case 'cropRecommendation':
                return <CropCard data={data} />;
            case 'marketPrice':
                return <MarketPriceCard {...data} />;
            case 'governmentScheme':
                return <SchemeCard {...data} />;
            case 'financialInsight':
                return <FinanceCard {...data} />;
            case 'confirmation':
                return <ConfirmationCard {...data} />;
            case 'genericCard':
                return (
                    <div className="voice-card">
                        <div className="voice-card-header">
                            <span className="voice-card-title">{data.title}</span>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                            {data.items && data.items.map((item, idx) => (
                                <div key={idx} style={{
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    borderBottom: idx < data.items.length - 1 ? '1px solid rgba(0,0,0,0.05)' : 'none',
                                    paddingBottom: '4px'
                                }}>
                                    <span style={{ fontWeight: '600', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                                        {item.label}:
                                    </span>
                                    <span style={{ fontWeight: '500', color: 'var(--text-primary)', textAlign: 'right' }}>
                                        {item.value}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                );
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
                        <p style={{ fontSize: '1.1rem', marginBottom: '8px' }}>👋 नमस्ते! KisanMitra में आपका स्वागत है</p>
                        <p style={{ fontSize: '0.9rem' }}>🎤 Click the mic to speak or type below...</p>
                        <p style={{ fontSize: '0.85rem', marginTop: '12px', opacity: 0.7 }}>
                            Try: "प्याज की कीमत क्या है?" or "Which crop should I grow?"
                        </p>
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

                {/* Loading Indicator */}
                {isLoading && (
                    <div className="message-bubble message-ai" style={{ opacity: 0.6 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <div className="typing-indicator">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                            <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                                KisanMitra is processing...
                            </span>
                        </div>
                    </div>
                )}

                <div ref={chatEndRef} />
            </div>

            {/* Input Bar - Fixed Bottom */}
            <div className="input-bar">
                <input
                    type="text"
                    placeholder={isRecording ? "🔴 Recording..." : "Type in Hindi or English... (Press Enter)"}
                    className="text-input"
                    value={inputText}
                    onChange={(e) => onInputChange(e.target.value)}
                    onKeyPress={handleKeyPress}
                    disabled={isLoading || isRecording}
                />
                <button
                    className="send-btn"
                    onClick={handleSendClick}
                    disabled={!inputText.trim() || isLoading || isRecording}
                    style={{
                        padding: '10px 16px',
                        backgroundColor: 'var(--color-primary-green)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '12px',
                        cursor: (inputText.trim() && !isLoading && !isRecording) ? 'pointer' : 'not-allowed',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        opacity: (inputText.trim() && !isLoading && !isRecording) ? 1 : 0.5
                    }}
                >
                    <Send size={20} />
                </button>
                <button
                    className="mic-btn-small"
                    onClick={onMicClick}
                    disabled={isLoading}
                    style={{
                        backgroundColor: isRecording ? '#D32F2F' : 'var(--color-accent-ochre)',
                        animation: isRecording ? 'pulse 1.5s infinite' : 'none'
                    }}
                    title={isRecording ? 'Stop Recording' : 'Start Recording'}
                >
                    {isRecording ? <Square size={24} /> : <Mic size={24} />}
                </button>
            </div>
        </div>
    );
};

export default ConversationView;
