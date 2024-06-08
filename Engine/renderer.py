import pygame as pg
import pygame_gui as pgu
from Engine.DOM.document import Document
from Engine.DOM.element import Element
from Engine.html_parser import HTMLParser
from Engine.STR.renderer import StyledText
from config import WIN_WIDTH, WIN_HEIGHT
from typing import Tuple

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

        self.mouse_pos: Tuple[int, int] = pg.mouse.get_pos()
        self.lmb_pressed: bool = pg.mouse.get_pressed()[0]

    def move_scroll_x(self, scroll_x: float) -> None:
        self.scroll_x += scroll_x
        self.scroll_x = max(min(self.scroll_x, self.styled_text.rendered_text.get_width()-self.width), 0)

    def move_scroll_y(self, scroll_y: float) -> None:
        self.scroll_y += scroll_y
        self.scroll_y = max(min(self.scroll_y, self.styled_text.rendered_text.get_height()-self.height), 0)

    def render(self) -> pg.Surface:
        self.update_elements()

        self.display_surf: pg.Surface = pg.Surface((self.width, self.height))
        self.display_surf.blit(self.styled_text.rendered_text, (-self.scroll_x, -self.scroll_y))

        return self.display_surf

    def search_children(self, element: Element) -> None:
        if element is None: return

        if element.rect.collidepoint(self.mouse_pos):
            if not element.rect_unused.collidepoint(self.mouse_pos):
                element.hovered = True

                if self.lmb_pressed: element.pressed = True
        else:
            element.hovered = False
            element.pressed = False
        
        for child in element.children:
            child.hovered = element.hovered
            child.pressed = element.pressed

            self.search_children(child)

    def update_elements(self) -> None:
        self.mouse_pos = pg.mouse.get_pos()
        self.lmb_pressed = pg.mouse.get_pressed()[0]

        self.search_children(self.html_parser.document.html_element)

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