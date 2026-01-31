import { History } from '../types/Types'

const FolderIcon = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gray-600">
        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
    </svg>
);

export default function ChatHistory() {
    let history: History[] = [
        { id: 1, title: "Hello world", timestamp: "8/29/2024, 10:26:51 AM", chatDiretory: "../../../log/" },
        { id: 1, title: "Hello world", timestamp: "8/29/2024, 10:26:51 AM", chatDiretory: "../../../log/" },
        { id: 1, title: "Hello world", timestamp: "8/29/2024, 10:26:51 AM", chatDiretory: "../../../log/" },
        { id: 1, title: "Hello world", timestamp: "8/29/2024, 10:26:51 AM", chatDiretory: "../../../log/" },
        { id: 1, title: "Hello world", timestamp: "8/29/2024, 10:26:51 AM", chatDiretory: "../../../log/" },
        { id: 1, title: "Hello world", timestamp: "8/29/2024, 10:26:51 AM", chatDiretory: "../../../log/" },
        { id: 1, title: "Hello world", timestamp: "8/29/2024, 10:26:51 AM", chatDiretory: "../../../log/" },
        { id: 1, title: "Hello world", timestamp: "8/29/2024, 10:26:51 AM", chatDiretory: "../../../log/" },
    ]

    return (
        <div className="p-4 bg-[#e4e4f8] rounded-t-xl flex flex-col h-1/2">
            <p className="text-sm text-gray-500 pb-1">Conversation History</p>
            <p className="text-xs text-gray-500 pb-1">Chat histories are stored locally. Deletion can be done manually in the location of each file</p>
            <div className="flex flex-col gap-3 p-4 overflow-y-auto">
                {history.map((hstr) => (
                    <div className="flex bg-white rounded-lg px-4 py-3 shadow-sm text-sm text-gray-700 items-center w-max-fit">
                        <div>
                            {hstr.title}
                            <div className="text-[10px] text-gray-400 mt-1">
                                {hstr.timestamp}
                            </div>
                        </div>
                        <FolderIcon />
                    </div>
                ))
                }
            </div>
        </div>
    );
}
