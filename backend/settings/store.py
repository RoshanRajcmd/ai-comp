# backend/settings/store.py
from .schema import Settings

_current_settings = Settings()

def get_settings() -> Settings:
    return _current_settings

def update_settings(new_settings: Settings):
    global _current_settings
    _current_settings = new_settings
