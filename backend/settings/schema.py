# backend/settings/schema.py
from pydantic import BaseModel
from typing import Literal

class Settings(BaseModel):
    mode: Literal["neuro", "evil_neuro"] = "neuro"
    chaos: float = 0.5          # 0.0 → calm, 1.0 → unhinged
    web_access: bool = True
