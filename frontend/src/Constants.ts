import NEUTRAL from './assets/emotions/neutral.png'
import HAPPY from './assets/emotions/happy.png'
import ANGRY from './assets/emotions/angry.png'
import PROUD from './assets/emotions/proud.png'
import SAD from './assets/emotions/sad.png'
import UNPLEASANT from './assets/emotions/unpleasant.png'
import EXCITED from './assets/emotions/excited.png'
import ERROR from './assets/emotions/error.png'
import { Emotion } from './types/Types'

export const AVT_EXPRESSIONS: Record<Emotion, string> = {
    neutral: NEUTRAL,
    happy: HAPPY,
    angry: ANGRY,
    proud: PROUD,
    sad: SAD,
    unpleasant: UNPLEASANT,
    excited: EXCITED,
    error: ERROR
};
