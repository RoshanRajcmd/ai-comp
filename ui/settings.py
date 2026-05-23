import json
import os
import copy
from nicegui import ui
from constants import (
    TEXT_MODEL, VISION_MODEL, PERSONA,
    CHAT_MEMORY_ENABLED, ENABLE_WEB_ACCESS, LCD_ENABLED,
)
from core.ollama_client import list_models
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Dict
from constants import DEFAULT_CONFIG, CONFIG_PATH
async def settings_page():
    models = await list_models()

    with ui.column().classes("w-full max-w-2xl mx-auto p-8 gap-6"):
        ui.label("Settings").classes("text-2xl font-bold")

        # Model selection
        with ui.card().classes("w-full p-4"):
            ui.label("Models").classes("text-lg font-semibold mb-2")
            ui.select(
                options=models,
                value=TEXT_MODEL,
                label="Text Model",
            ).classes("w-full")
            ui.select(
                options=models,
                value=VISION_MODEL,
                label="Vision Model",
            ).classes("w-full mt-2")

        # Persona
        with ui.card().classes("w-full p-4"):
            ui.label("Persona").classes("text-lg font-semibold mb-2")
            ui.input(
                value=PERSONA,
                label="Persona Name",
            ).classes("w-full")
            ui.textarea(
                lable="System Prompt",
                placeholder="Define Ollie's personality",
            ).classes("w-full mt-2").props("rows=4")

        # Toggles
        with ui.card().classes("w-full p-4"):
            ui.label("Features").classes("text-lg font-semibold mb-2")
            ui.switch("Chat Memory", value=CHAT_MEMORY_ENABLED)
            ui.switch("Web Access", value=ENABLE_WEB_ACCESS)
            ui.switch("LCD Enabled", value=LCD_ENABLED)

        # Save
        ui.button("Save", icon="save", on_click=lambda: save_settings()).props(
            "color=primary"
        )

def save_settings():
    # TODO: persists to config.json + reload runtime state
    ui.notify("Settings saved", type="positive")



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