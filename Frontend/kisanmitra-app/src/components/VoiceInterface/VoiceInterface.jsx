import React, { useState, useEffect, useRef } from 'react';
<<<<<<< HEAD
import { Mic, X, User, Send, Square } from 'lucide-react';
=======
import { Mic, X, User, Send } from 'lucide-react';
>>>>>>> c1b4d4f7ee534adf6060dab2218e32041e433534
import './styles/voice-interface.css';
import IdleHome from './IdleHome';
import ListeningState from './ListeningState';
import ConversationView from './ConversationView';
<<<<<<< HEAD
import { processText, processAudio } from '../../services/voiceService';
import { getErrorMessage } from '../../services/api';
=======
>>>>>>> c1b4d4f7ee534adf6060dab2218e32041e433534

const VoiceInterface = ({ isOpen, onClose }) => {
    const [viewState, setViewState] = useState('idle'); // idle, listening, conversation
    const [messages, setMessages] = useState([]);
<<<<<<< HEAD
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState(null);
    const [isRecording, setIsRecording] = useState(false);

    // Refs for MediaRecorder
=======
    const [isProcessing, setIsProcessing] = useState(false);
    const [textInput, setTextInput] = useState('');
>>>>>>> c1b4d4f7ee534adf6060dab2218e32041e433534
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

<<<<<<< HEAD
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
=======
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
>>>>>>> c1b4d4f7ee534adf6060dab2218e32041e433534
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
<<<<<<< HEAD
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
=======
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
>>>>>>> c1b4d4f7ee534adf6060dab2218e32041e433534
                )}
            </div>
        </div>
    );
};

export default VoiceInterface;
