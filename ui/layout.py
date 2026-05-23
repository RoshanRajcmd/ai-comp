from nicegui import ui

def layout():
    with ui.header().classes("items-center justify-between px-4 py-2 bg-gray-900"):
        ui.lable("Ollie").classes("text-xl font-bold text-white")
        with ui.row().classes("gap-4"):
            ui.link("Chat", "/").classes("text-white no-underline hover:text-blue-300")
            ui.link("Settings", "/settings").classes("text-white no-underline hover:text-blue-300")