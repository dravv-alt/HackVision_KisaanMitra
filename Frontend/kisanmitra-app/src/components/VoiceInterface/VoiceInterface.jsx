import React, { useState, useEffect, useRef } from 'react';
import { Mic, X, User, Send, Square } from 'lucide-react';
import './styles/voice-interface.css';
import IdleHome from './IdleHome';
import ListeningState from './ListeningState';
import ConversationView from './ConversationView';
import { processText, processAudio } from '../../services/voiceService';
import { getErrorMessage } from '../../services/api';

const VoiceInterface = ({ isOpen, onClose }) => {
    const [viewState, setViewState] = useState('idle'); // idle, listening, conversation
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState(null);
    const [isRecording, setIsRecording] = useState(false);

    // Refs for MediaRecorder
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);

    // Reset state when opened
    useEffect(() => {
        if (isOpen) {
            setViewState('idle');
            setMessages([]);
            setInputText('');
            setSessionId(`session_${Date.now()}`);
        }
    }, [isOpen]);

    // Cleanup speech synthesis on unmount
    useEffect(() => {
        return () => {
            if (window.speechSynthesis) {
                window.speechSynthesis.cancel();
            }
        };
    }, []);

    // Text-to-Speech Function
    const speakText = (text) => {
        if (!window.speechSynthesis) {
            console.warn('Text-to-speech not supported');
            return;
        }

        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);

        // Auto-detect language or default to Hindi
        // If text contains mostly English characters, switch to en-IN
        const isEnglish = /^[a-zA-Z0-9\s.,?!'"]+$/.test(text.substring(0, 50));
        utterance.lang = isEnglish ? 'en-IN' : 'hi-IN';

        utterance.rate = 1.0;
        utterance.pitch = 1.0;

        window.speechSynthesis.speak(utterance);
    };

    // Handle text input submission
    const handleTextSubmit = async (text) => {
        if (!text.trim() || isLoading) return;

        const userMessage = {
            type: 'user',
            text: text,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };

        // Add user message immediately
        setMessages(prev => [...prev, userMessage]);
        setInputText('');
        setViewState('conversation');
        setIsLoading(true);

        try {
            // Call voice agent API with text
            const response = await processText(text, 'F001', sessionId);
            console.log("Voice Agent Response (Text):", response);

            // Parse and add AI response
            const aiMessage = parseVoiceResponse(response);
            setMessages(prev => [...prev, aiMessage]);

            // Speak response
            if (response.explanation_hindi) {
                speakText(response.explanation_hindi);
            } else if (response.explanation_english) {
                speakText(response.explanation_english);
            }

        } catch (error) {
            console.error('Voice agent error:', error);
            const errorMessage = {
                type: 'ai',
                text: `❌ ${getErrorMessage(error)}`,
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    // Handle audio recording using Native MediaRecorder
    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
            mediaRecorderRef.current = mediaRecorder;
            audioChunksRef.current = [];

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data);
                }
            };

            mediaRecorder.onstop = handleRecordingStop;

            mediaRecorder.start();
            setIsRecording(true);
            setViewState('listening');

        } catch (error) {
            console.error('Failed to start recording:', error);
            alert('Microphone access denied or browser not supported. Please allow microphone permissions.');
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            // Also stop all tracks
            if (mediaRecorderRef.current.stream) {
                mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
            }
            setIsRecording(false);
        }
    };

    const handleRecordingStop = async () => {
        try {
            setViewState('conversation');

            // Create Blob from chunks
            const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });

            // Create File object
            const audioFile = new File([audioBlob], 'voice-recording.webm', {
                type: 'audio/webm',
                lastModified: Date.now()
            });

            // Show user message placeholder
            const userMessage = {
                type: 'user',
                text: '🎤 ...',  // Placeholder while processing
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            };
            setMessages(prev => [...prev, userMessage]);
            setIsLoading(true);

            // Send audio to backend
            const response = await processAudio(audioFile, 'F001', sessionId);
            console.log("Voice Agent Response (Audio):", response);

            // Update user message with transcription (prefer English translation)
            setMessages(prev => {
                const updated = [...prev];
                const lastUserMsg = updated[updated.length - 1];
                if (lastUserMsg && lastUserMsg.type === 'user' && lastUserMsg.text === '🎤 ...') {
                    // Use English translation if available, else raw transcription
                    const displayText = response.metadata?.user_input_english || response.transcription || 'Audio processed';
                    lastUserMsg.text = `🎤 "${displayText}"`;
                }
                return updated;
            });

            // Add AI response
            const aiMessage = parseVoiceResponse(response);
            setMessages(prev => [...prev, aiMessage]);

            // Speak response
            if (response.explanation_hindi) {
                speakText(response.explanation_hindi);
            } else if (response.explanation_english) {
                speakText(response.explanation_english);
            }

        } catch (error) {
            console.error('Audio processing error:', error);
            // Remove processing placeholder if error
            setMessages(prev => prev.filter(msg => msg.text !== '🎤 ...'));

            const errorMessage = {
                type: 'ai',
                text: `❌ Audio Error: ${getErrorMessage(error)}`,
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const cancelRecording = () => {
        if (isRecording && mediaRecorderRef.current) {
            if (mediaRecorderRef.current.stream) {
                mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
            }
            mediaRecorderRef.current.onstop = null; // Prevent handling
            mediaRecorderRef.current.stop();
            setIsRecording(false);
        }
        setViewState(messages.length > 0 ? 'conversation' : 'idle');
    };

    // Parse backend voice response to frontend format
    const parseVoiceResponse = (response) => {
        const cards = [];
        const cropCards = [];

        // Convert backend cards to frontend format
        if (response.cards && Array.isArray(response.cards)) {
            response.cards.forEach(card => {
                try {
                    const frontendCard = mapBackendCardToFrontend(card);
                    if (frontendCard) {
                        if (frontendCard.type === 'cropRecommendation') {
                            cropCards.push(frontendCard);
                        } else {
                            cards.push(frontendCard);
                        }
                    }
                } catch (e) {
                    console.error("Error mapping card:", card, e);
                }
            });

            // If multiple crop cards, create a summary Generic Card
            if (cropCards.length > 1) {
                const items = cropCards.map((c, idx) => ({
                    label: `${idx + 1}. ${c.data.name}`,
                    value: c.data.expected ? c.data.expected : 'Recommended'
                }));

                cards.unshift({
                    type: 'genericCard',
                    data: {
                        title: 'Top Crop Recommendations',
                        items: items
                    }
                });
            } else if (cropCards.length === 1) {
                // If only one, just show it normally
                cards.unshift(cropCards[0]);
            }
        }

        // Use Hindi explanation as primary text
        const displayText = response.explanation_hindi || response.explanation_english || response.reasoning || 'Response received';

        return {
            type: 'ai',
            text: displayText,
            cardData: cards.length > 0 ? cards[0] : null,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            context: response.metadata?.context || null
        };
    };

    /**
     * GENERIC CARD MAPPER
     * Maps backend details dictionary directly to a list of key-values
     * Formats: Title : Content
     */
    const mapBackendCardToFrontend = (backendCard) => {
        if (!backendCard) return null;

        // Extract data
        const cardType = (backendCard.card_type || '').toLowerCase();
        // SUPPORT BOTH 'details' AND 'data'
        const rawData = backendCard.details || backendCard.data || {};

        // Always use the Generic Card Structure for consistent "Title: Content" display
        // We filter out internal fields and format keys for display
        const displayItems = Object.entries(rawData)
            .filter(([key, value]) => {
                // Filter out non-displayable or internal fields
                const skipKeys = ['trend_hindi', 'crop_name_hindi', 'scheme_name_hindi', 'reasons', 'risks'];
                return value !== null && value !== '' && !skipKeys.includes(key);
            })
            .map(([key, value]) => {
                // Format Key: "crop_name" -> "Crop Name"
                const label = key
                    .split('_')
                    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                    .join(' ');

                // Format Value: Handle booleans, arrays, etc.
                let displayValue = value;
                if (typeof value === 'boolean') displayValue = value ? 'Yes' : 'No';
                if (Array.isArray(value)) displayValue = value.join(', ');
                if (typeof value === 'number' && (key.includes('price') || key.includes('amount') || key.includes('expense'))) {
                    displayValue = `₹${value.toLocaleString('en-IN')}`;
                }

                return { label, value: displayValue };
            });

        // Use a Generic Card Type that simply renders the list
        return {
            type: 'genericCard', // We will update ConversationView to handle this
            data: {
                title: backendCard.title || 'Information',
                items: displayItems
            }
        };
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
                    <span style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>
                        KisanMitra Voice {isRecording && '🔴 Recording...'}
                    </span>
                    <div style={{ width: '32px', height: '32px', borderRadius: '50%', backgroundColor: '#ddd', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <User size={18} />
                    </div>
                </div>

                {/* Content Area */}
                {viewState === 'idle' && (
                    <IdleHome onMicClick={startRecording} />
                )}

                {viewState === 'listening' && (
                    <ListeningState
                        onCancel={cancelRecording}
                        isRecording={isRecording}
                        onStop={stopRecording}
                    />
                )}

                {viewState === 'conversation' && (
                    <ConversationView
                        messages={messages}
                        onMicClick={isRecording ? stopRecording : startRecording}
                        inputText={inputText}
                        onInputChange={setInputText}
                        onSubmit={handleTextSubmit}
                        isLoading={isLoading}
                        isRecording={isRecording}
                    />
                )}
            </div>
        </div>
    );
};

export default VoiceInterface;
