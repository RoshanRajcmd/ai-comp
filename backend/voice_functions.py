import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from piper.voice import PiperVoice
import time
import io

# --- 1. CONFIGURATION ---
# Faster-Whisper (Speech-to-Text)
WHISPER_MODEL_SIZE = "tiny" 
WHISPER_DEVICE = "cpu"

# Piper (Text-to-Speech)
PIPER_MODEL_PATH = "assets/en_US-lessac-medium.onnx" # CHANGE THIS PATH
PIPER_CONFIG_PATH = "assets/en_US-lessac-medium.onnx.json" # CHANGE THIS PATH

# Audio Recording (for sounddevice)
SAMPLE_RATE = 16000  # Whisper is optimized for 16000 Hz
CHANNELS = 1
RECORD_SECONDS = 5
SILENCE_THRESHOLD = 500  # Adjust based on your mic sensitivity

# --- 2. INITIALIZATION ---

# Load Whisper Model (runs once at startup)
whisper_model = WhisperModel(WHISPER_MODEL_SIZE, device=WHISPER_DEVICE, compute_type="int8")

# Load Piper Voice (runs once at startup)
piper_voice = PiperVoice.load(PIPER_MODEL_PATH, config_path=PIPER_CONFIG_PATH)


# --- 3. SPEECH-TO-TEXT (Listening) ---

def listen_and_transcribe():
    """
    Records audio from the microphone until a timeout, then transcribes it.
    (Note: Real-time Voice Activity Detection (VAD) is more complex but better)
    """
    print("🤖 Listening... Speak now.")
    
    # Simple recording block (records for a fixed time)
    recording = sd.rec(int(RECORD_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype=np.int16)
    sd.wait() # Wait until recording is finished
    
    print("🤖 Transcribing...")
    
    # Save the recording to a temporary buffer (Whisper needs audio data)
    audio_data = recording.flatten().astype(np.float32) / 32768.0
    
    # Transcribe the audio
    segments, info = whisper_model.transcribe(
        audio_data, 
        language="en", 
        beam_size=5
    )
    
    # Aggregate all segments into a single string
    transcript = " ".join(segment.text.strip() for segment in segments)
    
    return transcript.strip()


# --- 4. TEXT-TO-SPEECH (Talking) ---

def speak_text(text_to_speak):
    """
    Uses Piper to generate speech and streams it directly to the speaker.
    """
    print(f"🤖 Speaking: {text_to_speak}")
    
    # Piper yields raw PCM data chunks
    audio_stream = piper_voice.synthesize_stream_raw(text_to_speak)
    
    # Setup sounddevice output stream
    with sd.OutputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16') as stream:
        for chunk in audio_stream:
            # Piper chunks are bytes, convert to numpy array for sounddevice
            np_chunk = np.frombuffer(chunk, dtype=np.int16)
            stream.write(np_chunk)
            
    # The 'with' statement closes the stream automatically when finished
    print("🤖 Finished speaking.")

# --- 5. DEMO (The Orchestration Snippet) ---

if __name__ == "__main__":
    
    # The full sequence will be: Listen -> Process (Ollama) -> Speak
    
    # 1. Listening Phase
    user_input = listen_and_transcribe()
    print(f"\nUser said: **{user_input}**\n")
    
    if user_input:
        # 2. Ollama Processing would go here (or, for this demo, a placeholder)
        
        # Simulating the LLM response with the expression tag
        llm_response = f"[HAPPY] That is a very interesting thing to say about: {user_input}."
        
        # Expression Tag Extraction (as shown in the previous step)
        try:
            tag_end = llm_response.find(']')
            dialogue = llm_response[tag_end+1:].strip()
            # In your main script, you would call draw_companion(tag) here
            
            # 3. Speaking Phase
            speak_text(dialogue)
            
        except Exception as e:
            print(f"Error processing LLM response: {e}")

    else:
        print("No speech detected or could not transcribe.")