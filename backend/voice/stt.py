import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

# --- 1. CONFIGURATION ---
WHISPER_MODEL_SIZE = "tiny"
WHISPER_DEVICE = "cpu"
SAMPLE_RATE = 16000
CHANNELS = 1
RECORD_SECONDS = 5

# --- 2. INITIALIZATION ---
whisper_model = WhisperModel(WHISPER_MODEL_SIZE, device=WHISPER_DEVICE, compute_type="int8")

def listen_and_transcribe():
    """
    Records audio from the microphone until a timeout, then transcribes it.
    """
    print("🤖 Listening... Speak now.")
    
    recording = sd.rec(int(RECORD_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=np.int16)
    sd.wait()
    
    print("🤖 Transcribing...")
    
    audio_data = recording.flatten().astype(np.float32) / 32768.0
    
    segments, info = whisper_model.transcribe(
        audio_data, 
        language="en", 
        beam_size=5
    )
    
    transcript = " ".join(segment.text.strip() for segment in segments)
    
    return transcript.strip()