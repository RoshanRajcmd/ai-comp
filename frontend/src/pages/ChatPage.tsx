import { useState, useEffect } from "react";
import AvatarPane from "./AvatarPane";
import ChatMessages from "./ChatMessages";
import { Emotion } from "../types/Types";
import ChatHistory from "./ChatHistory";
import { History } from "../types/Types";

const HamburgerIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
    </svg>
);

const CloseIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
    </svg>
);

export default function ChatPage() {
    const [emotion, setEmotion] = useState<Emotion>("neutral");
    const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null);
    const [conversationTitle, setConversationTitle] = useState<string>("");
    const [conversations, setConversations] = useState<History[]>([]);
    const [isHistoryOpen, setIsHistoryOpen] = useState(false);

    const handleCreateNewChat = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/conversations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title: 'New Conversation' })
            });

            const data = await response.json();

            if (data.id) {
                setSelectedConversationId(data.id);
                setConversationTitle(data.title);
                setConversations([{ id: data.id, title: data.title, timestamp: data.timestamp }, ...conversations]);
            }
        } catch (err) {
            console.error('Failed to create new conversation:', err);
        }
    };

    const handleSelectConversation = (convId: string, conversation?: History) => {
        setSelectedConversationId(convId);
        if (conversation) {
            setConversationTitle(conversation.title);
            setConversations(prev => {
                // Update conversations list to include this one
                const existing = prev.find(c => c.id === convId);
                if (existing) {
                    return prev;
                }
                return [...prev, conversation];
            });
        }
        // Close mobile history panel when a conversation is selected
        setIsHistoryOpen(false);
    };

    const handleSaveTitle = async (newTitle: string) => {
        if (!selectedConversationId) return;

        try {
            const response = await fetch(`http://localhost:5000/api/conversations/${selectedConversationId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title: newTitle })
            });

            if (response.ok) {
                setConversationTitle(newTitle);
                // Update conversations list with new title
                setConversations(prev =>
                    prev.map(c =>
                        c.id === selectedConversationId ? { ...c, title: newTitle } : c
                    )
                );
            } else {
                console.error('Failed to update conversation title');
            }
        } catch (err) {
            console.error('Failed to save title:', err);
        }
    };

    return (
        <div className="flex h-screen">
            {/* Main Content Area */}
            <div className="flex-1 flex flex-col bg-[#EAEAF3] relative">
                {/* Mobile Hamburger Button */}
                <div className="lg:hidden flex items-center p-2 bg-[#EAEAF3] border-b">
                    <button
                        onClick={() => setIsHistoryOpen(!isHistoryOpen)}
                        className="p-2 text-gray-700 hover:text-gray-900"
                        title="Toggle conversation history"
                    >
                        {isHistoryOpen ? <CloseIcon /> : <HamburgerIcon />}
                    </button>
                </div>

                <AvatarPane emotion={emotion} />
                <ChatMessages
                    conversationId={selectedConversationId}
                    conversationTitle={conversationTitle}
                    onCreateNewChat={handleCreateNewChat}
                    onSaveTitle={handleSaveTitle}
                    onEmotionChange={(emotion) => {
                        setEmotion(emotion);
                    }}
                />
            </div>

            {/* Mobile Overlay - Chat History Modal */}
            {isHistoryOpen && (
                <div
                    className="fixed inset-0 bg-black bg-opacity-50 lg:hidden z-40"
                    onClick={() => setIsHistoryOpen(false)}
                />
            )}

            {/* Chat History Sidebar - Desktop fixed, Mobile toggleable */}
            <div
                className={`flex fixed lg:static right-0 top-0 h-screen w-80 lg:w-auto bg-[#e4e4f8] transform transition-transform duration-300 z-50 lg:z-0 ${isHistoryOpen ? "translate-x-0" : "translate-x-full lg:translate-x-0"
                    }`}
            >
                <ChatHistory onSelectConversation={handleSelectConversation} />
            </div>
        </div>
    );
}
