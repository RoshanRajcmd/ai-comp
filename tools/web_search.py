import requests
from bs4 import BeautifulSoup

def scrape_url(url: str, max_chars: int = 3000) -> str:
    try:
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (compatible; Ollie/1.0)"
        })
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Remove non-content elements
        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        # Collapse blank lines and truncate
        lines = [line for line in text.splitlines() if line.strip()]
        content = "\n".join(lines)

        if len(content) > max_chars:
            content = content[:max_chars] + "\n...(truncated)"

        return content
    except Expection as e:
        return f"Scrape failed: {e}"