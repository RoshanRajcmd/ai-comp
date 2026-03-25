import json
import os
import copy
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Dict
from constants import DEFAULT_CONFIG, CONFIG_PATH

class OllamaConfig(BaseModel):
    keep_alive: str
    num_thread: int
    temperature: float = Field(ge=0.0, le=2.0)
    top_k: int
    top_p: float

class Settings(BaseModel):
    persona: str
    text_model: str
    vision_model: str
    voice_model: str
    chat_memory: bool
    camera_rotation: int
    extra_preset_prompt: str
    web_access: bool
    ollama_config: OllamaConfig

def load_settings() -> Settings:
    config = copy.deepcopy(DEFAULT_CONFIG)

    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                user_config = json.load(f)
                print(f"Loaded user config: {user_config}")
                if user_config:
                    config.update(user_config)
        else:
            print("Config.json does not exist. Using default configuration")
    except Exception as e:
        print(f"Config Error: {e}")

    return Settings(**config)

def save_settings_to_file(settings: Settings):
    print(f"Saving settings to: {CONFIG_PATH}")
    with open(CONFIG_PATH, "w") as f:
        json.dump(settings.model_dump(), f, indent=4)
    print("Settings persisted successfully.")

def detect_changes(old: Settings, new: Settings):
    changes = {}

    old_dict = old.model_dump()
    new_dict = new.model_dump()

    for key in new_dict:
        if old_dict.get(key) != new_dict.get(key):
            print("Found Changes in setting")
            changes[key] = {
                "old": old_dict.get(key),
                "new": new_dict.get(key)
            }

    return changes

def update_settings(new_settings: Settings):
    global _settings

    old_settings = _settings
    changed = detect_changes(old_settings, new_settings)

    save_settings_to_file(new_settings)
    _settings = load_settings()
    print("Settings Changes with new setting", _settings)
    return changed

# Global singleton
_settings = load_settings()
def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = load_settings()
        print("Initial load of setting is successfull")
    print("Fetched setting: ", _settings)
    return _settings