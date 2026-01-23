import React, { useState, useEffect, useRef } from 'react';
import { Mic, X, User, Send } from 'lucide-react';
import './styles/voice-interface.css';
import IdleHome from './IdleHome';
import ListeningState from './ListeningState';
import ConversationView from './ConversationView';

const VoiceInterface = ({ isOpen, onClose }) => {
    const [viewState, setViewState] = useState('idle'); // idle, listening, conversation
    const [messages, setMessages] = useState([]);
    const [isProcessing, setIsProcessing] = useState(false);
    const [textInput, setTextInput] = useState('');
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);

    // Reset state when opened
    useEffect(() => {
        if (isOpen) {
            setViewState('idle');
            setMessages([]);
        }
    }, [isOpen]);

    const startListening = async () => {
        setViewState('listening');

        try {
            // Request microphone permission
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

            // Create MediaRecorder
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorderRef.current = mediaRecorder;
            audioChunksRef.current = [];

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data);
                }
            };

            mediaRecorder.onstop = async () => {
                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());

                // Create audio blob
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });

                // Send to backend
                await processAudioInput(audioBlob);
            };

            // Start recording
            mediaRecorder.start();

            // Auto-stop after 10 seconds (optional)
            setTimeout(() => {
                if (mediaRecorder.state === 'recording') {
                    mediaRecorder.stop();
                }
            }, 10000);

        } catch (error) {
            console.error('Error accessing microphone:', error);
            alert('Could not access microphone. Please check permissions.');
            setViewState('idle');
        }
    };

    const stopListening = () => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
            mediaRecorderRef.current.stop();
        }
    };

    const cancelListening = () => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
            mediaRecorderRef.current.stop();
            audioChunksRef.current = [];
        }
        setViewState(messages.length > 0 ? 'conversation' : 'idle');
    };

    const processAudioInput = async (audioBlob) => {
        setIsProcessing(true);
        setViewState('conversation');

        try {
            // Create FormData
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.webm');
            formData.append('farmer_id', 'F001'); // TODO: Get from auth context

            // Send to backend
            const response = await fetch('http://localhost:8000/api/v1/voice/process-audio', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Failed to process audio');
            }

            const data = await response.json();

            // Add user message (transcribed text)
            if (data.user_input) {
                addMessage('user', data.user_input);
            }

            // Add AI response
            if (data.response_text) {
                addMessage('ai', data.response_text, data.card_data, {
                    duration: data.audio_duration || 5,
                    transcript: data.response_text
                }, data.context_used);
            }

        } catch (error) {
            console.error('Error processing audio:', error);
            addMessage('ai', 'माफ़ करें, मुझे आपकी बात समझने में समस्या हुई। कृपया फिर से कोशिश करें।');
        } finally {
            setIsProcessing(false);
        }
    };

    const processTextInput = async (text) => {
        if (!text.trim()) return;

        setIsProcessing(true);
        setTextInput('');

        // Add user message immediately
        addMessage('user', text);

        try {
            const response = await fetch('http://localhost:8000/api/v1/voice/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    hindi_text: text,
                    farmer_id: 'F001', // TODO: Get from auth context
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to process text');
            }

            const data = await response.json();

            // Add AI response
            if (data.response_text) {
                addMessage('ai', data.response_text, data.card_data, {
                    duration: data.audio_duration || 5,
                    transcript: data.response_text
                }, data.context_used);
            }

        } catch (error) {
            console.error('Error processing text:', error);
            addMessage('ai', 'माफ़ करें, मुझे आपकी बात समझने में समस्या हुई। कृपया फिर से कोशिश करें।');
        } finally {
            setIsProcessing(false);
        }
    };

    const handleTextSubmit = (e) => {
        e.preventDefault();
        if (textInput.trim() && !isProcessing) {
            processTextInput(textInput);
        }
    };

    const addMessage = (type, text, cardData = null, audio = null, context = null) => {
        setMessages(prev => [...prev, {
            type,
            text,
            cardData,
            audio,
            transcript: audio?.transcript,
            context,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }]);
    };

    if (!isOpen) return null;

    return (
        <div className="voice-interface-overlay" onClick={(e) => {
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
                    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '20px' }}>
                        <ListeningState onCancel={cancelListening} />
                        <button
                            onClick={stopListening}
                            style={{
                                padding: '12px 24px',
                                backgroundColor: '#4CAF50',
                                color: 'white',
                                border: 'none',
                                borderRadius: '8px',
                                cursor: 'pointer',
                                fontSize: '16px',
                                fontWeight: 'bold'
                            }}
                        >
                            बोलना बंद करें (Stop Speaking)
                        </button>
                    </div>
                )}

                {viewState === 'conversation' && (
                    <>
                        <ConversationView messages={messages} onMicClick={startListening} />

                        {/* Text Input Area */}
                        <div style={{
                            padding: '16px',
                            borderTop: '1px solid #e0e0e0',
                            backgroundColor: 'white'
                        }}>
                            <form onSubmit={handleTextSubmit} style={{ display: 'flex', gap: '8px' }}>
                                <input
                                    type="text"
                                    value={textInput}
                                    onChange={(e) => setTextInput(e.target.value)}
                                    placeholder="अपना सवाल टाइप करें... (Type your question...)"
                                    disabled={isProcessing}
                                    style={{
                                        flex: 1,
                                        padding: '12px 16px',
                                        border: '1px solid #ddd',
                                        borderRadius: '24px',
                                        fontSize: '14px',
                                        outline: 'none'
                                    }}
                                />
                                <button
                                    type="submit"
                                    disabled={isProcessing || !textInput.trim()}
                                    style={{
                                        padding: '12px 20px',
                                        backgroundColor: isProcessing || !textInput.trim() ? '#ccc' : '#4CAF50',
                                        color: 'white',
                                        border: 'none',
                                        borderRadius: '24px',
                                        cursor: isProcessing || !textInput.trim() ? 'not-allowed' : 'pointer',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '8px'
                                    }}
                                >
                                    <Send size={18} />
                                    {isProcessing ? 'भेज रहे हैं...' : 'भेजें'}
                                </button>
                            </form>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default VoiceInterface;
