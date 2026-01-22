import React, { useState } from 'react';
import FloatingMicButton from './VoiceInterface/FloatingMicButton';
import VoiceInterface from './VoiceInterface/VoiceInterface';

const VoiceAgent = () => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <>
            {/* The Trigger Button - Always visible */}
            {!isOpen && <FloatingMicButton onClick={() => setIsOpen(true)} />}

            {/* The Full Interface Modal */}
            <VoiceInterface
                isOpen={isOpen}
                onClose={() => setIsOpen(false)}
            />
        </>
    );
};

export default VoiceAgent;
