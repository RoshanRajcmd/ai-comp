import json
import os

PERSONA_FILE = 'config.json'

DEFAULT_PERSONAS = {
    "ollie": {
        "name": "ollie",
        "pronouns": "she/her",
        "personality": "Cute, playful, curious, slightly naive.",
    }
    "oliver": {
        "name": "Oliver",
        "pronouns": "he/him",
        "personality": "Sarcastic, mischievous, gently teaseful.",
    },
}

def get_personas() -> dict:
    if os.path.exists(PERSONA_FILE):
        try:
            with open(PERSONA_FILE, "r") as f:
                data = json.load(f)
            return data.get("persona", DEFAULT_PERSONAS)
        except Exception:
            pass
    return DEFAULT_PERSONAS

def get_person(name: str) -> dict:
    personas = get_personas()
    return personas.get(name, personas.get("ollie"))

def format_persona_block(name: str) -> str:
    p = get_person(name)
    return (
        f"You are {p['name']}.\n"
        f"Pronouns: {p['pronouns']}\n"
        f"Personality: {p['personality']}\n"
    )

def save_persona(name: str, pronouns: str, personality: str):
    if os.path.exists(PERSONA_FILE):
        with open(PERSONA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    if "personas" not in data:
        data["personas"] = DEFAULT_PERSONAS

    data["personas"][name.lower()] = {
        "name": name,
        "pronouns": pronouns,
        "personality": personality,
    }

    with open(PERSONA_FILE, "w") as f:
        json.dump(data, f, indent=4)
