
from Engine.html_parser import HTMLParser

class Renderer:
    def __init__(self) -> None:
        self.url: str = ""

    def load_page(self, url: str) -> None:
        self.url = url

        raw_html = self.request_page_contents()

        parsed_html = 