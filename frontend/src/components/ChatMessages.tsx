import { useState } from "react";
import { ChatMessage } from "./Types";
import { MdContentCopy } from "react-icons/md";
import { LuSendHorizontal } from "react-icons/lu";
//import ChatInput from "./ChatInput";

export default function ChatMessages() {

    let messages: ChatMessage[] = [
        { id: 1, sender: "bot", text: "Sure! I can help with that." },
        { id: 2, sender: "bot", text: "Let me look into that for you." },
        { id: 3, sender: "bot", text: "Interesting question!" },
        { id: 4, sender: "bot", text: "I’ll get back to you on that." },
        { id: 5, sender: "bot", text: "Thanks for your message!" },];

    const [message, setMessage] = useState<string>("");

    function onSend() {

    }

    return (
        <div className="flex flex-col gap-4 p-4 h-1/2">
            <div className="flex flex-col gap-4 p-4 overflow-y-auto">
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
            </div>
            {/* ChatInput  */}
            <div className="justify-center items-center">
                <div className="flex items-center gap-2 p-4 border-t">
                    <input
                        className="flex-1 border rounded-lg p-2 text-sm"
                        placeholder="Enter to send..."
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && onSend()}
                    />
                    <button
                        className="flex gap-1 p-2 bg-blue-500 text-white hover:bg-blue-400 rounded-lg text-sm shadow items-center"
                        onClick={onSend}
                    >
                        <LuSendHorizontal />
                        Send
                    </button>
                </div>
                <button
                    className="flex gap-1 p-2 bg-blue-500 text-white hover:bg-blue-400 rounded-lg text-sm shadow items-center">
                    <MdContentCopy />
                    Copy Chat
                </button>
            </div>
        </div>
    );
}
