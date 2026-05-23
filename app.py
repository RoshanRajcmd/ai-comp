from nicegui, import ui, app
from constants import HOST, PORT
from ui.layout import layout
from ui.chat import chat_page
from ui.settings import settings_page

@ui.page("/")
def index():
    layout()
    chat_page()

@ui.page("/settings")
def settings():
    layout()
    settings_page()

if __name__ in ("__main__", "__mp_main__"):
    ui.run(
        host=HOST,
        port=PORT,
        title="Ollie",
        favicon="/assets/favicon.png",
        dark=True,
        reload=True, #Hot reload during dev, set False in prod
    )