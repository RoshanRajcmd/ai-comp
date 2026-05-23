from nicegui import ui
from constants import EXPRESSIONS

class AvatarPane:
    def __init__(self):
        self.current_expression = "neutral"
        self.image_element = None
        self._build()

    def _build(self):
        with ui.column().classes("w-64 h-full items-center justify-center justify-center bg-gray-800 p-4"):
            self.image_element = ui.image(
                f"assests/faces/{EXPRESSIONS['neutral']}"
            ).classes("w-48 h-48 rounded-full")
            self.status_label = ui.label("Idle").classes("text-gray-400 mt-4 text-sm")

    def set_expression(self, emotion: str):
        if emotion not in EXPRESSIONS:
            emotion = "neutral"
        self.current_expression = emotion
        self.image_element.set_source(f"assests/faces/{EXPRESSIONS[emotion]}")
        self.status_label.set_text(emotion.capitalize())

    def avatar_pane() -> AvatarPane:
        return AvatarPane()