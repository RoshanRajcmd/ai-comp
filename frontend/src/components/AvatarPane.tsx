import { useState, useEffect, useRef } from 'react';
import { FaMicrophone } from "react-icons/fa";
import { FaSquare } from "react-icons/fa";
import { AVT_EXPRESSIONS } from './Constants';
import { default as languageCodesData } from '@/data/language-codes.json';
import { default as countryCodesData } from '@/data/country-codes.json';

export default function AvatarPane() {
    const recognitionRef = useRef<SpeechRecognition>();

    const [action, setAction] = useState("");
    const [imageSrc, setImageSrc] = useState(AVT_EXPRESSIONS["netural"]);
    const [isActive, setIsActive] = useState<boolean>(false);
    const [text, setText] = useState<string>();
    const [response, setResponse] = useState<string>();
    const [voices, setVoices] = useState<Array<SpeechSynthesisVoice>>();
    const [language, setLanguage] = useState<string>('pt-BR');


    const changeImage = () => {
        setImageSrc(AVT_EXPRESSIONS["happy"]);
    };

    async function sleep(ms: number): Promise<void> {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }

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
        // setAction("Listening")
        // await sleep(2000)
        // setAction("Speaking")
        // await sleep(2000)
        // setAction("")

        if (isActive) {
            recognitionRef.current?.stop();
            setIsActive(false);
            return;
        }

        speak(' ');

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognitionRef.current = new SpeechRecognition();

        recognitionRef.current.onstart = function () {
            setIsActive(true);
        }

        recognitionRef.current.onend = function () {
            setIsActive(false);
        }

        recognitionRef.current.onresult = async function (event) {
            const transcript = event.results[0][0].transcript;

            setText(transcript);

            // const results = await fetch('/api/processInput', {
            //     method: 'POST',
            //     body: JSON.stringify({
            //     })
            // }).then(r => r.json());
            const results = { text: "Test response" }
            setResponse(results.text);

            speak(results.text);
        }

        recognitionRef.current.start();
    }

    function speak(text: string) {
        const utterance = new SpeechSynthesisUtterance(text);

        if (activeVoice) {
            utterance.voice = activeVoice;
        };

        window.speechSynthesis.speak(utterance);
    }

    return (
        <div className="flex-1 rounded-2xl shadow-lg flex flex-col w-1/2 mx-4 my-4 bg-[#EAEAF3] border-r border-gray-200 p-4">
            <h2 className="text-xl font-semibold pb-2">Ai Companion bot</h2>
            <p className="text-xs text-gray-500 mb-1">Offline Model: Mistral from ollama</p>

            <div className="flex-1 my-6 p-6 bg-white rounded-lg shadow-sm text-sm text-gray-700 text-center">
                <div className='w-full flex items-center justify-center'>
                    <img
                        src={imageSrc}
                        className='size-60 object-cover'
                    />
                </div>
                <div className="text-[10px] text-gray-400 mt-1">
                    {action}
                </div>
            </div>
            <div className="flex flex-col justify-center items-center">
                <button className="w-fit bg-white rounded-full p-6 shadow-sm text-sm hover:bg-slate-100" onClick={handleMicPress}>
                    {action == "Speaking" ? <FaSquare size='25px' /> : <FaMicrophone size='25px' />}
                </button>
                {/* there are 3 state for action - listening, speaking, null (shows Press to Speak) */}
                <span className="text-sm font-light text-gray-500 py-6">{action == "" ? "Press to Speak" : action}</span>
            </div>
        </div >
    );
}
