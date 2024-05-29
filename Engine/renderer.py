import pygame as pg
import pygame_gui as pgu
from Engine.DOM.document import Document
from Engine.html_parser import HTMLParser
from Engine.STR.renderer import StyledText
from config import WIN_WIDTH, WIN_HEIGHT
from math import floor
from typing import List

class Renderer:
    def __init__(self, manager: pgu.UIManager, width: int, height: int):
        self.manager: pgu.UIManager = manager
        self.styled_text: StyledText = StyledText("\n", width, height, (0, 0, 0), (255, 255, 255), "Arial", 16, (2, 20, 2, 20))
        self.html_parser: HTMLParser = HTMLParser(self.manager, self.styled_text, width, height)
        self.display_surf: pg.Surface = pg.Surface((width, height))

        self.width: int = width
        self.height: int = height

        self.scroll_x: float = 0.0
        self.scroll_y: float = 0.0

    def render(self) -> pg.Surface:
        self.display_surf: pg.Surface = pg.Surface((self.width, self.height))
        self.display_surf.blit(self.styled_text.rendered_text, (-self.scroll_x, -self.scroll_y))

        return self.display_surf

    def loadHTML(self, html: str) -> Document | None:
        self.scroll_x = 0.0
        self.scroll_y = 0.0
        
        # clear text
        self.styled_text.clear()

        document: Document = self.html_parser.parseHTML(html)

        return document
    
    def loadHTML_NonBlocking(self, html: str, mutable_document_class: Document) -> None:
        loaded_html: Document | None = self.loadHTML(html)
        
        if loaded_html is not None:
            mutable_document_class = loaded_html