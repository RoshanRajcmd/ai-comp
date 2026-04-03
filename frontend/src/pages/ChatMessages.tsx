import React, { useState, useRef, useEffect } from "react";
import { ChatMessage, Emotion } from "../types/Types";
import { MdEditDocument } from "react-icons/md";

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
    readonly onEmotionChange: (emotion: Emotion) => void;
    readonly conversationId?: string | null;
    readonly conversationTitle?: string;
    readonly onCreateNewChat?: () => void;
    readonly onSaveTitle?: (newTitle: string) => void;
}

export default function ChatMessages({ onEmotionChange, conversationId, conversationTitle, onCreateNewChat, onSaveTitle }: Readonly<ChatMessagesProps>) {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [message, setMessage] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [loadingHistory, setLoadingHistory] = useState<boolean>(false);
    const [isEditing, setIsEditing] = useState(false);
    const [editedTitle, setEditedTitle] = useState(conversationTitle || "");
    const [creatingNew, setCreatingNew] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    // Update edited title when conversation title changes
    useEffect(() => {
        setEditedTitle(conversationTitle || "");
        setIsEditing(false);
    }, [conversationTitle]);

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

    // Load conversation when selected
    useEffect(() => {
        if (conversationId) {
            loadConversation(conversationId);
        } else {
            setMessages([]);
        }
    }, [conversationId]);

    const loadConversation = async (convId: string) => {
        try {
            setLoadingHistory(true);
            const response = await fetch(`http://localhost:5000/api/conversations/${convId}`);
            const data = await response.json();

            if (data.messages) {
                // Convert backend message format to ChatMessage format
                const formattedMessages: ChatMessage[] = data.messages.map((msg: { role: string; content: string }, idx: number) => ({
                    id: idx,
                    sender: msg.role === 'user' ? 'user' : 'bot',
                    text: msg.content
                }));
                setMessages(formattedMessages);
            }
        } catch (error) {
            console.error('Failed to load conversation:', error);
        } finally {
            setLoadingHistory(false);
        }
    };

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
                body: JSON.stringify({
                    prompt: message,
                    conversation_id: conversationId || undefined
                })
            });

            const data = await response.json();
            console.log('Backend response:', data);

            if (data.response) {
                const botMsg: ChatMessage = {
                    id: messages.length + 2,
                    sender: "bot",
                    text: data.response,
                    expression: data.expression,
                };

                onEmotionChange(data.expression || "neutral");
                setMessages(prev => [...prev, botMsg]);

                // If we got a conversation_id back, update it (for new conversations)
                if (data.conversation_id && !conversationId) {
                    // Notify parent that a new conversation was created
                    console.log('New conversation created:', data.conversation_id);
                }
            } else if (data.error) {
                // Add error message to chat
                const errorMsg: ChatMessage = {
                    id: messages.length + 2,
                    sender: "bot",
                    text: `Error: ${data.error}`
                };
                setMessages(prev => [...prev, errorMsg]);
                onEmotionChange("error");
                console.error('Backend error:', data.error);
            } else {
                // Unexpected response format
                const errorMsg: ChatMessage = {
                    id: messages.length + 2,
                    sender: "bot",
                    text: `Error: Unexpected response format`
                };
                setMessages(prev => [...prev, errorMsg]);
                onEmotionChange("error");
            }
        } catch (error) {
            console.error('Failed to send message:', error);
            const errorMsg: ChatMessage = {
                id: messages.length + 2,
                sender: "bot",
                text: `Connection error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`
            };
            setMessages(prev => [...prev, errorMsg]);
            onEmotionChange("error");
        } finally {
            setLoading(false);
        }
    }

    const copyChat = () => {
        const chatText = messages
            .map(msg => `${msg.sender === 'user' ? 'You' : 'Bot'}: ${msg.text}`)
            .join('\n');

        navigator.clipboard.writeText(chatText).then(() => {
            alert('Chat copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy chat:', err);
        });
    };

    const handleCreateNewChat = async () => {
        try {
            setCreatingNew(true);
            await onCreateNewChat?.();
        } finally {
            setCreatingNew(false);
        }
    };

    const handleSaveTitle = () => {
        if (editedTitle.trim()) {
            onSaveTitle?.(editedTitle.trim());
            setIsEditing(false);
        }
    };

    const handleCancelEdit = () => {
        setEditedTitle(conversationTitle || "");
        setIsEditing(false);
    };

    return (
        <div className="flex flex-col p-4 h-full">
            {/* Header */}
            <div className="flex items-center justify-between mb-4 pb-4 border-b">
                <div className="flex-1">
                    {isEditing ? (
                        <div className="flex items-center gap-2">
                            <input
                                type="text"
                                value={editedTitle}
                                onChange={(e) => setEditedTitle(e.target.value)}
                                className="flex-1 border rounded-lg p-2 text-sm"
                                autoFocus
                                onKeyDown={(e) => {
                                    if (e.key === "Enter") handleSaveTitle();
                                    if (e.key === "Escape") handleCancelEdit();
                                }}
                            />
                            <button
                                onClick={handleSaveTitle}
                                className="px-3 py-1 bg-green-500 text-white rounded-lg text-sm hover:bg-green-400"
                            >
                                Save
                            </button>
                            <button
                                onClick={handleCancelEdit}
                                className="px-3 py-1 bg-gray-400 text-white rounded-lg text-sm hover:bg-gray-500"
                            >
                                Cancel
                            </button>
                        </div>
                    ) : (
                        <div className="flex items-center gap-2">
                            <h2 className="text-lg font-semibold text-gray-700">
                                {conversationTitle || "Untitled"}
                            </h2>
                            {conversationTitle && (
                                <button
                                    onClick={() => setIsEditing(true)}
                                    className="p-1 text-gray-500 hover:text-gray-700"
                                    title="Edit conversation title"
                                >
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L21 6.5z"></path>
                                    </svg>
                                </button>
                            )}
                        </div>
                    )}
                </div>
                <button
                    onClick={handleCreateNewChat}
                    disabled={creatingNew}
                    className="flex items-center gap-2 p-2 bg-blue-500 text-white hover:bg-blue-400 rounded-lg text-sm shadow transition-all disabled:bg-gray-400"
                    title="Create new chat"
                >
                    <MdEditDocument size={20} />
                    {creatingNew ? 'Creating...' : 'New'}
                </button>
            </div>

            {loadingHistory && (
                <div className="flex items-center justify-center p-4 text-gray-500">
                    Loading conversation...
                </div>
            )}
            <div className="flex-1 flex flex-col gap-4 p-4 overflow-y-auto">
                {messages.length === 0 && !loadingHistory && (
                    <div className="flex items-center justify-center h-full text-gray-400">
                        {conversationId ? 'No messages in this conversation' : 'Start typing to begin'}
                    </div>
                )}
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
                    className="flex gap-1 p-2 bg-blue-500 text-white hover:bg-blue-400 rounded-lg text-sm shadow items-center"
                    onClick={copyChat}
                >
                    <CopyIcon />
                    Copy Chat
                </button>
            </div>
        </div>
    );
}
