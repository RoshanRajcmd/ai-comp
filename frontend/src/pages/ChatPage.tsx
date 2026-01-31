import AvatarPane from "./AvatarPane";
import ChatMessages from "./ChatMessages";
import ChatHistory from "./ChatHistory";

export default function ChatPage() {
    return (
        <div className="flex max-h-screen bg-gradient-to-br from-indigo-200 to-blue-200">
            <AvatarPane />

            {/* Sidebar  */}
            <div className="flex-1 flex flex-col bg-white">
                <ChatMessages />
                <ChatHistory />
            </div>
        </div >
    );
}
