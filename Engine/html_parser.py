from Engine.DOM.document import Document
from Engine.DOM.element import Element
from typing import List
from bs4 import BeautifulSoup, element
from pygame_gui import UIManager
from Ui.elements import USE_TEXTBOX_TAGS, TEXT_TAGS
from Engine.STR.renderer import StyledText
from config import WIDTH, HEIGHT

class HTMLParser:
    def __init__(self, manager: UIManager):
        self.document: Document = Document()
        self.manager: UIManager = manager
        self.styled_text: StyledText = StyledText("\n", WIDTH, HEIGHT, (0, 0, 0), (255, 255, 255), "Calibri", 16, (2, 5, 2, 5))
        self.curr_y: int = 50

    def recurse_tag_children(self, tag: element.Tag):
        for child_tag in tag.children:
            if isinstance(child_tag, element.Tag):
                child_tag.attrs["tag"] = child_tag.name
                child_tag.attrs["text"] = child_tag.text
                child_tag.attrs["html"] = str(child_tag)

                if child_tag.name in TEXT_TAGS:
                    self.styled_text.html_text += f"{child_tag.attrs['html']}\n"
                    continue

                self.recurse_tag_children(child_tag)
        
    def parseHTML(self, html: str):
        soup = BeautifulSoup(html, 'html.parser')

        first_elem = soup.find()

        self.recurse_tag_children(first_elem)
        self.styled_text.render()

        return self.document