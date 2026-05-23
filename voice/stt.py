from faster_whisper import WhisperModel

_model = None

def _get_model() -> WhisperModel:
    global _model
    if _model is None:
        _model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
        )
    return _model

def transcribe(audio_path: str) -> str:
    # Transcribe audio file to text
    model = _get_model()

    segments, _ = model.transcribe(
        audio_path,
        language = "en",
        beam_size = 3,
        vad_filter = True,
    )

    text = " ".join(segment.text.strip() for segment in segments)
    return text