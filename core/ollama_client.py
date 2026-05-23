import json
import ollama
from constants import OLLAMA_API_URL, TEXT_MODEL, OLLAMA_CONFIG
from core.prompt_builder import build_messages

client = ollama.AsyncClient(host=OLLAMA_API_URL)

async def stream_response(user_message: str):
    messages = build_messages(user_message)

    stream = await client.chat(
        model=TEXT_MODEL,
        messages=messages,
        stream=True,
        options={
            "num_thread":OLLAMA_CONFIG["num_thread"],
            "temperature":OLLAMA_CONFIG["temperature"],
            "top_k":OLLAMA_CONFIG["top_k"],
            "top_p":OLLAMA_CONFIG["top_p"],
        },
        keep_alive=OLLAMA_CONFIG["keep_alive"],
    )

    async for chuck in stream:
        content = chuck["message"]["content"]
        if content:
            yield content

def parse_response(raw: str) -> dict:
    # Extract expression from JSON response, or fallback to neutral.
    try:
        data = json.loads(raw)
        return {
            "response":data.get("response", ""),
            "expression":data.get("expression", "neutral"),
        }
    except (json.JSONDecodeError, TypeError):
        return {
            "response": raw,
            "expression": "error",
        }

async def list_models() -> list[str]:
    response = await client.list()
    return [m["name"] for m in response["models"]]

async def check_model_available(model: str) -> bool:
    models = await list_models()
    return model in models