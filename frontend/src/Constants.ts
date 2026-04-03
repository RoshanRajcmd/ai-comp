import NEUTRAL from './assets/emotions/neutral.png'
import HAPPY from './assets/emotions/happy.png'
import ANGRY from './assets/emotions/angry.png'
import PROUD from './assets/emotions/proud.png'
import SAD from './assets/emotions/sad.png'
import UNPLEASANT from './assets/emotions/unpleasant.png'
import EXCITED from './assets/emotions/excited.png'
import ERROR from './assets/emotions/error.png'
import { Emotion } from './types/Types'

export const GREETING_SOUND_DIR = "sounds/greeting_sounds"
export const ACK_SOUND_DIR = "sounds/ack_sounds"
export const THINKING_SOUND_DIR = "sounds/thinking_sounds"
export const ERROR_SOUND_DIR = "sounds/error_sounds"


enum ModelState {
    IDLE,
    LISTENING,
    THINKING,
    SPEAKING,
    ERROR,
    CAPTURING,
    WARMUP
}

export const AVT_EXPRESSIONS: Record<Emotion, string> = {
    neutral: NEUTRAL,
    happy: HAPPY,
    angry: ANGRY,
    proud: PROUD,
    sad: SAD,
    unpleasant: UNPLEASANT,
    excited: EXCITED,
    listening: NEUTRAL, // Placeholder, no specific asset found
    capturing: NEUTRAL, // Placeholder, no specific asset found
    warmingup: NEUTRAL,  // Placeholder, no specific asset found
    error: ERROR,
};