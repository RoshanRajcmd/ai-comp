import json

DEFAULT_RESPONSE = {
    "text": "",
    "emotion": "neutral"
}

def parse_llm_response(raw: str):
    try:
        data = json.loads(raw)

        return {
            "text": data.get("text", ""),
            "emotion": data.get("emotion", "neutral")
        }

    except Exception:
        # Fallback if model misbehaves
        return {
            **DEFAULT_RESPONSE,
            "text": raw
        }
