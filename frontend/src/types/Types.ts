export type Emotion =
    | "neutral"
    | "happy"
    | "angry"
    | "sad"
    | "excited"
    | "proud"
    | "unpleasant"
    | "error"
    | "listening"
    | "capturing"
    | "warmingup";


export type ChatMessage = {
    id: number
    sender: "user" | "bot"
    text: string
    expression?: Emotion
}


export interface History {
    id: string;
    title: string;
    timestamp: string;
    message_count?: number;
}

export interface Conversation {
    id: string;
    title: string;
    timestamp: string;
    messages: Array<{
        role: "user" | "assistant";
        content: string;
    }>;
}