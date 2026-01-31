declare global {
    interface Window {
        webkitSpeechRecognition: any;
        SpeechRecognition: any;
    }

    // Minimal SpeechRecognition type
    interface SpeechRecognition extends EventTarget {
        lang: string;
        continuous: boolean;
        interimResults: boolean;
        maxAlternatives: number;
        start(): void;
        stop(): void;
        abort(): void;
        onaudiostart?: (event: Event) => void;
        onsoundstart?: (event: Event) => void;
        onspeechstart?: (event: Event) => void;
        onspeechend?: (event: Event) => void;
        onsoundend?: (event: Event) => void;
        onaudioend?: (event: Event) => void;
        onresult?: (event: SpeechRecognitionEvent) => void;
        onerror?: (event: SpeechRecognitionErrorEvent) => void;
        onnomatch?: (event: SpeechRecognitionEvent) => void;
    }
}

export { };
