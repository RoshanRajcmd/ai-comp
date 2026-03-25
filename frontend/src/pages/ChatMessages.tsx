import React, { useState, useRef, useEffect } from "react";
import { ChatMessage, Emotion } from "../types/Types";

const SendIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-white">
        <line x1="22" y1="2" x2="11" y2="13"></line>
        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
    </svg>
);

const CopyIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-white">
        <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
        <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
    </svg>
);

interface ChatMessagesProps {
    onEmotionChange: (emotion: Emotion) => void;
}

export default function ChatMessages({ onEmotionChange }: ChatMessagesProps) {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [message, setMessage] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    // Check backend health on component mount
    React.useEffect(() => {
        fetch('http://localhost:5000/api/health')
            .then(r => r.json())
            .then(data => {
                if (data.status !== 'ok') {
                    console.warn('Backend health check failed:', data);
                }
            })
            .catch(e => console.error('Cannot reach backend:', e));
    }, []);

    async function onSend() {
        if (!message.trim()) return;

        // Add user message to chat
        const userMsg: ChatMessage = {
            id: messages.length + 1,
            sender: "user",
            text: message
        };
        setMessages([...messages, userMsg]);
        setMessage("");
        setLoading(true);

        console.log('Sending message:', message);

        try {
            // Send message to backend
            const response = await fetch('http://localhost:5000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: message })
            });

            const data = await response.json();
            console.log('Backend response:', data);
            if (data) {
                const botMsg: ChatMessage = {
                    id: messages.length + 2,
                    sender: "bot",
                    text: data.response,
                    expression: data.expression,
                };

                onEmotionChange(data.expression);
                setMessages(prev => [...prev, botMsg]);

            } else {
                // Add error message to chat
                const errorMsg: ChatMessage = {
                    id: messages.length + 2,
                    sender: "bot",
                    text: `Error: ${data.error || 'Unknown error'}`
                };
                setMessages(prev => [...prev, errorMsg]);
                onEmotionChange("error");
                console.error('Backend error:', data.error);
            }
        } catch (error) {
            console.error('Failed to send message:', error);
            const errorMsg: ChatMessage = {
                id: messages.length + 2,
                sender: "bot",
                text: `Connection error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`
            };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="flex flex-col gap-4 p-4 h-full">
            <div className="flex-1 flex flex-col gap-4 p-4 overflow-y-auto">
                {messages.map((msg) => (
                    <div
                        key={msg.id}
                        className={`max-w-xs p-3 rounded-lg text-sm ${msg.sender === "user"
                            ? "bg-blue-100 self-end"
                            : "bg-gray-100 self-start"
                            }`}
                    >
                        {msg.text}
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>
            {/* ChatInput  */}
            <div className="flex flex-col justify-center items-center gap-2">
                <div className="flex items-center gap-2 p-4 border-t w-full">
                    <input
                        className="flex-1 border rounded-lg p-2 text-sm"
                        placeholder="Enter to send..."
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && onSend()}
                        disabled={loading}
                    />
                    <button
                        className="flex gap-1 p-2 bg-blue-500 text-white hover:bg-blue-400 rounded-lg text-sm shadow items-center disabled:bg-gray-400"
                        onClick={onSend}
                        disabled={loading}
                    >
                        <SendIcon />
                        {loading ? "Sending..." : "Send"}
                    </button>
                </div>
                <button
                    className="flex gap-1 p-2 bg-blue-500 text-white hover:bg-blue-400 rounded-lg text-sm shadow items-center">
                    <CopyIcon />
                    Copy Chat
                </button>
            </div>
        </div>
    );
}
