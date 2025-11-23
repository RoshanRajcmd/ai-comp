export interface ChatMessage {
    id: number;
    sender: "user" | "bot";
    text: string;
}

export interface History {
    id: number;
    title: string;
    timestamp: string;
    chatDiretory: string;
}