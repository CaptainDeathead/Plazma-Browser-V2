from bs4 import BeautifulSoup
from bs4.element import Tag

from Engine.DOM.document import Document
from Engine.DOM.element import Element

class HTMLParser:
    def __init__(self) -> None:
        self.document: Document = Document()

    def parse_bs4_tree(self, bs4_elem: Tag) -> Element:
        ...

    def parse_html(self, html: str) -> None:
        parent_bs4_elem = BeautifulSoup(html, "html.parser")

        parsed_element = self.parse_bs4_tree(parent_bs4_elem)

        self.document.set_parent_element()