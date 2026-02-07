import { useState } from "react";
import AvatarPane from "./AvatarPane";
import ChatMessages from "./ChatMessages";
import { Emotion } from "../types/Types";
import ChatHistory from "./ChatHistory";

export default function ChatPage() {
    const [emotion, setEmotion] = useState<Emotion>("neutral");

    return (
        <div className="flex max-h-screen bg-gradient-to-br from-indigo-200 to-blue-200">
            <AvatarPane emotion={emotion} />


            {/* Sidebar  */}
            <div className="flex-1 flex flex-col bg-white">
                <ChatMessages
                    onEmotionChange={(emotion) => {
                        setEmotion(emotion);
                    }}
                />
                <ChatHistory />
            </div>
        </div >
    );
}
