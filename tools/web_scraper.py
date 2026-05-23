import requests
from bs4 import BeautifulSoup

class WebScraper:
    def scrape(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
