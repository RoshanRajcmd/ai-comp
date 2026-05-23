from nicegui import ui
from core.ollama_client import stream_response
from core.chat_history import get_history, save_message
from ui.avatar import avatar_pane

async def send_message(message_input, message_container, avatar):
    text = message_input.value.strip()
    if not text:
        return

    message_input.value = ""

    with message_container:
        ui.chat_message(text, name="You", sent=True)
    message_container.scroll_to(percent=1.0)
    save_message("user", text)

    avatar.set_expression("thinking")

    response_text = ""
    with message_container:
        response_msg = ui.chat_message(name="Ollie", sent=False)

    async for chunk in stream_response(text):
        response_text += chunk
        response_msg.clea()
        with response_msg:
            ui.markdown(response_text)
        message_container.scroll_to(percent=1.0)

    save_message("assistant", response_text)
    avatar.set_expression("neutral")

def chat_page():
    with ui.row().classes("w-full h-[calc(100vh-64px)] gap-0"):
        avatar = avatar_pane()
        with ui.column().classes("flex-1 h-full"):
            message_container = ui.scroll_area().classes("flex-1 w-full p-4")
            with message_container:
                for msg in get_history():
                    ui.chat_message(
                        msg["content"],
                        name="You" if msg["role"] == "user" else "Ollie",
                        sent=(msg["role"] == "user"),
                    )

            with ui.row().classes("w-full p-4 gap-2 items-center border-t border-gray-700"):
                message_input = ui.input(placeholder="Message Ollie...").props(
                    "outlined dense"
                ).classes("flex-1").on(
                    "Keydown.enter",
                    lambda: send_message(message_input, message_container, avatar),
                )
                ui.button(icon="send", on_click=lambda: send_message(
                    message_input, message_container, avatar
                )).props("flat round color=primary")
                ui.button("Live", icon="mic", on_click=lambda: toggle_live(avatar)).props(
                    "flat round color=green"
                )

def toggle_live(avatar):
    # TODO: will wire to voice/stt.py and voice/tts.py
    avatar.set_expression("listening")
    ui.notify("Live mode - coming soon", type="info")