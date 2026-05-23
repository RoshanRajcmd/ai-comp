import subprocess
import tempfile
import os
from pathlib import Path
from constants import VOICE_MODEL

def synthesize(text: str) -> str:
    if not text.strip():
        return None

    output_path = os.path.join(tempfile.gettempdir(), "ollie_tts.wav")

    try:
        subprocess.run(
            [
                "piper",
                "--model", VOICE_MODEL,
                "--output_file", output_path,
            ],
            input=text,
            text=True,
            capture_output=True,
            timeout=30,
        )
        if os.path.exists(output_path):
            return output_path
        return None

    except (subprocess.TimeoutExpired) as e:
        print(f"TTS failed: {e}")
        return None

def synthesize_chucks(text: str):
    # Split text into sentences and yield WAV paths for streaming playback.
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for i, sentences in enumerate(sentences):
        if not sentence.strip():
            continue

        output_path = os.path.join(tempfile.gettempdir(), f"ollie_tts_{i}.wav")

        try:
            subprocess.run(
                [
                    "piper",
                    "--model", VOICE_MODEL,
                    "--output_file", output_path,
                ],
                input=sentence,
                text=True,
                capture_output=True,
                timeout=30,
            )
            if os.path.exists(output_path):
                yield output_path

        except Exception:
            continue