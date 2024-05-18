import pygame as pg
import pygame_gui as pgu
from Engine.DOM.document import Document
from Engine.html_parser import HTMLParser
from Engine.STR.renderer import StyledText
from config import WIN_WIDTH, WIN_HEIGHT

class Renderer:
    def __init__(self, manager: pgu.UIManager):
        self.manager: pgu.UIManager = manager
        self.styled_text: StyledText = StyledText("\n", WIN_WIDTH, WIN_HEIGHT, (0, 0, 0), (255, 255, 255), "Arial", 16, (2, 20, 2, 20))
        self.html_parser: HTMLParser = HTMLParser(self.manager, self.styled_text)

    def loadHTML(self, html: str) -> Document | None:
        # clear text
        self.styled_text.clear()

        return self.html_parser.parseHTML(html)
    
    def loadHTML_NonBlocking(self, html: str, mutable_document_class: Document) -> None:
        loaded_html: Document | None = self.loadHTML(html)
        
        if loaded_html is not None:
            mutable_document_class = loaded_html