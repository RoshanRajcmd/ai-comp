import { useState, useEffect } from "react";
import AvatarPane from "./AvatarPane";
import ChatMessages from "./ChatMessages";
import { Emotion } from "../types/Types";
import ChatHistory from "./ChatHistory";
import { History } from "../types/Types";

export default function ChatPage() {
    const [emotion, setEmotion] = useState<Emotion>("neutral");
    const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null);
    const [conversationTitle, setConversationTitle] = useState<string>("");
    const [conversations, setConversations] = useState<History[]>([]);

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
    };

    const handleSaveTitle = async (newTitle: string) => {
        // Update title in backend - implement if your backend supports this
        setConversationTitle(newTitle);
        // You can add an API call here to persist the title change
    };

    return (
        <div className="flex h-screen">
            <div className="justify-center">
                <AvatarPane emotion={emotion} />
                <ChatHistory onSelectConversation={handleSelectConversation} />
            </div>

            {/* Sidebar  */}
            <div className="flex-1 flex flex-col bg-[#EAEAF3]">
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
        </div >
    );
}
