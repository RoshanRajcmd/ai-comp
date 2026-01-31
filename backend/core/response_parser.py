import json

DEFAULT_RESPONSE = {
    "text": "",
    "emotion": "neutral",
    "intensity": 0.5
}

def parse_llm_response(raw: str):
    try:
        data = json.loads(raw)

        return {
            "text": data.get("text", ""),
            "emotion": data.get("emotion", "neutral"),
            "intensity": float(data.get("intensity", 0.5))
        }

    except Exception:
        # Fallback if model misbehaves
        return {
            **DEFAULT_RESPONSE,
            "text": raw
        }
