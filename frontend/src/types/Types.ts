export type ChatMessage = {
    id: number
    sender: "user" | "bot"
    text: string
    emotion?: string
    intensity?: number
}


export interface History {
    id: number;
    title: string;
    timestamp: string;
    chatDiretory: string;
}