export type Emotion =
    | "neutral"
    | "happy"
    | "angry"
    | "sad"
    | "excited"
    | "proud"
    | "unpleasant"
    | "error";


export type ChatMessage = {
    id: number
    sender: "user" | "bot"
    text: string
    emotion?: Emotion
}


export interface History {
    id: number;
    title: string;
    timestamp: string;
    chatDiretory: string;
}