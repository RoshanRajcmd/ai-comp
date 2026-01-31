import { useState, useEffect, useRef } from 'react';
import { AVT_EXPRESSIONS } from '../Constants';

declare global {
    interface Window {
        SpeechRecognition: any;
        webkitSpeechRecognition: any;
    }
}

const MicrophoneIcon = () => (
    <svg width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gray-800">
        <path d="M12 1a3 3 0 0 0-3 3v12a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
        <line x1="12" y1="19" x2="12" y2="23"></line>
        <line x1="8" y1="23" x2="16" y2="23"></line>
    </svg>
);

const StopIcon = () => (
    <svg width="25" height="25" viewBox="0 0 24 24" fill="currentColor" className="text-gray-800">
        <rect x="6" y="6" width="12" height="12"></rect>
    </svg>
);

export default function AvatarPane() {
    const recognitionRef = useRef<SpeechRecognition | null>(null);

    const [action, setAction] = useState("");
    const [imageSrc, setImageSrc] = useState(AVT_EXPRESSIONS["netural"]);
    const [isActive, setIsActive] = useState<boolean>(false);
    const [voices, setVoices] = useState<Array<SpeechSynthesisVoice>>();
    const [language, setLanguage] = useState<string>('pt-BR');
    // const lastBotMessage = [...messages]
    //     .reverse()
    //     .find(m => m.sender === "bot");
    // const emotion = lastBotMessage?.emotion || "neutral";
    // const intensity = lastBotMessage?.intensity || 0.5;


    const availableVoices = voices?.filter(({ lang }) => lang === language);
    const activeVoice =
        availableVoices?.find(({ name }) => name.includes('Google'))
        || availableVoices?.find(({ name }) => name.includes('Luciana'))
        || availableVoices?.[0];

    useEffect(() => {
        const voices = window.speechSynthesis.getVoices();
        if (Array.isArray(voices) && voices.length > 0) {
            setVoices(voices);
            return;
        }
        if ('onvoiceschanged' in window.speechSynthesis) {
            window.speechSynthesis.onvoiceschanged = function () {
                const voices = window.speechSynthesis.getVoices();
                setVoices(voices);
            }
        }
    }, []);

    function handleMicPress() {

        if (isActive) {
            recognitionRef.current?.stop();
            setIsActive(false);
            return;
        }

        speak(' ');

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognitionRef.current = new SpeechRecognition();

        recognitionRef.current!.addEventListener('start', function () {
            setIsActive(true);
        });

        recognitionRef.current!.addEventListener('end', function () {
            setIsActive(false);
        });

        recognitionRef.current!.addEventListener('result', async function (event: any) {
            const transcript = event.results[0][0].transcript;

            // const results = await fetch('/api/processInput', {
            //     method: 'POST',
            //     body: JSON.stringify({
            //     })
            // }).then(r => r.json());
            const results = { text: "Test response" };

            speak(results.text);
        });

        recognitionRef.current!.start();
    }

    function speak(text: string) {
        const utterance = new SpeechSynthesisUtterance(text);

        if (activeVoice) {
            utterance.voice = activeVoice;
        };

        window.speechSynthesis.speak(utterance);
    }

    function get_settings() {
        //TODO: Fetch from backend
        return {
            mode: "neuro",
            chaos: 0.5,
        }
    }

    return (
        <div className="flex-1 rounded-2xl shadow-lg flex flex-col w-1/2 mx-4 my-4 bg-[#EAEAF3] border-r border-gray-200 p-4">
            <h2 className="text-xl font-semibold pb-2">Ai Companion bot</h2>
            <p className="text-xs text-gray-500 mb-1">Model: {get_settings().mode} Persona: {get_settings().chaos}</p>

            <div className="flex-1 my-6 p-6 bg-white rounded-lg shadow-sm text-sm text-gray-700 text-center">
                <div className='w-full flex items-center justify-center'>
                    <img
                        src={imageSrc}
                        className='size-60 object-cover'
                        alt='AI Avatar'
                    />
                </div>
                <div className="text-[10px] text-gray-400 mt-1">
                    {action}
                </div>
            </div>
            <div className="flex flex-col justify-center items-center">
                <button className="w-fit bg-white rounded-full p-6 shadow-sm text-sm hover:bg-slate-100" onClick={handleMicPress}>
                    {action === "Speaking" ? <StopIcon /> : <MicrophoneIcon />}
                </button>
                {/* there are 3 state for action - listening, speaking, null (shows Press to Speak) */}
                <span className="text-sm font-light text-gray-500 py-6">{action === "" ? "Press to Speak" : action}</span>
            </div>
        </div >
    );
}
