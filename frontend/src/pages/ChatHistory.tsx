import { useEffect, useState } from 'react'
import { History } from '../types/Types'

const FolderIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gray-600">
        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
    </svg>
);

interface ChatHistoryProps {
    readonly onSelectConversation: (conversationId: string, conversation?: History) => void;
}

export default function ChatHistory({ onSelectConversation }: Readonly<ChatHistoryProps>) {
    const [history, setHistory] = useState<History[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedId, setSelectedId] = useState<string | null>(null);

    useEffect(() => {
        fetchConversations();
    }, []);

    const fetchConversations = async () => {
        try {
            setLoading(true);
            const response = await fetch('http://localhost:5000/api/conversations');
            const data = await response.json();

            if (data.conversations) {
                setHistory(data.conversations);
            }
            setError(null);
        } catch (err) {
            console.error('Failed to fetch conversations:', err);
            setError('Failed to load conversations');
        } finally {
            setLoading(false);
        }
    };

    const handleSelectConversation = (convId: string, conversation: History) => {
        setSelectedId(convId);
        onSelectConversation(convId, conversation);
    };

    const formatDate = (timestamp: string) => {
        try {
            const date = new Date(timestamp);
            return date.toLocaleString();
        } catch {
            return timestamp;
        }
    };

    return (
        <div className="p-4 bg-[#e4e4f8] rounded-t-xl flex flex-col h-1/2">
            <div className="flex items-center justify-between pb-2 gap-5">
                <div className=''>
                    <p className="text-base text-gray-500">Conversation History</p>
                    <p className="text-xs font-light italic text-gray-500">Chat histories are stored locally.<br />Deletion can be done manually in the location of each file</p>
                </div>
            </div>
            {error && <p className="text-xs text-red-500 pb-2">{error}</p>}
            {loading ? (
                <div className="flex items-center justify-center p-4 text-gray-500">Loading...</div>
            ) : (
                <div className="flex flex-col gap-3 p-4 overflow-y-auto">
                    {history.length === 0 ? (
                        <p className="text-xs text-gray-400">No conversations yet</p>
                    ) : (
                        history.map((hstr) => (
                            <button
                                key={hstr.id}
                                onClick={() => handleSelectConversation(hstr.id, hstr)}
                                className={`flex bg-white rounded-lg px-4 py-3 shadow-sm text-sm cursor-pointer transition-all text-left ${selectedId === hstr.id
                                    ? 'bg-blue-50 border-l-4 border-blue-500'
                                    : 'hover:bg-gray-50'
                                    } text-gray-700 items-center justify-between w-full`}
                            >
                                <div>
                                    <p className="font-medium truncate max-w-xs">{hstr.title}</p>
                                    <div className="text-[10px] text-gray-400 mt-1">
                                        {formatDate(hstr.timestamp)}
                                    </div>
                                </div>
                                <FolderIcon />
                            </button>
                        ))
                    )}
                </div>
            )}
        </div>
    );
}
