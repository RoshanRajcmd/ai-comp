import sounddevice as sd
import numpy as np
from piper.voice import PiperVoice

# --- 1. CONFIGURATION ---
PIPER_MODEL_PATH = "models/en_US-lessac-medium.onnx"
PIPER_CONFIG_PATH = "models/en_US-lessac-medium.onnx.json"
SAMPLE_RATE = 16000
CHANNELS = 1

# --- 2. INITIALIZATION ---
piper_voice = PiperVoice.load(PIPER_MODEL_PATH, config_path=PIPER_CONFIG_PATH)

def speak_text(text_to_speak):
    """
    Uses Piper to generate speech and streams it directly to the speaker.
    """
    print(f"🤖 Speaking: {text_to_speak}")
    
    audio_stream = piper_voice.synthesize_stream_raw(text_to_speak)
    
    with sd.OutputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16') as stream:
        for chunk in audio_stream:
            np_chunk = np.frombuffer(chunk, dtype=np.int16)
            stream.write(np_chunk)
            
    print("🤖 Finished speaking.")