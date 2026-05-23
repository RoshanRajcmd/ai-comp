import datetime
from tools.web_search import search_web
from tool.web_scraper import scrape_url

def dispatch(action_data: dict) -> str:
    action = action_data.get("action", "").lower().strip()
    value = action_data.get("value", "") or action_data.get("query", "")

    handlers = {
        "get_time": _handle_time,
        "search_web": _handle_search,
        "scrape_url": _handle_scrape,
        "capture_image": _handle_capture,
    }

    handler = handlers.get(action)
    if handler:
        return handler(value)
    return f"Unknown action: {action}"

def _handle_time(value: str) -> str:
    now = datetime.datetime.now().strftime("%I-%M-%p, %A:%B:%d")
    return f"The current time is {now}."

def _handle_search(query: str) -> str:
    if not query:
        return "No search query provided."
    results = search_web(query)
    return results

def _handle_scrape(url: str) -> str:
    if not url:
        return "No URL provided."
    return scrape_url(url)

def _handle_capture(value: str) -> str:
    # TODO: wire to rpicam-still when camera attached
    return "Camera not available."