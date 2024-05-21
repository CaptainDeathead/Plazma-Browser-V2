import pygame as pg
import pygame_gui as pgu
from Engine.DOM.document import Document
from Engine.html_parser import HTMLParser
from Engine.STR.renderer import StyledText
from config import WIN_WIDTH, WIN_HEIGHT
from math import floor
from typing import List
from copy import deepcopy

class Renderer:
    def __init__(self, manager: pgu.UIManager):
        self.manager: pgu.UIManager = manager
        self.styled_text: StyledText = StyledText("\n", WIN_WIDTH, WIN_HEIGHT, (0, 0, 0), (255, 255, 255), "Arial", 16, (2, 20, 2, 20))
        self.html_parser: HTMLParser = HTMLParser(self.manager, self.styled_text)
        self.display_surf: pg.Surface = pg.Surface((self.styled_text.wrap_px, self.styled_text.render_height*2))

        self.scroll_x: float = 0.0
        self.scroll_y: float = 0.0

    def render(self) -> pg.Surface:
        screen_index: int = floor(self.scroll_y / self.styled_text.render_height)

        if screen_index >= len(self.styled_text.rendered_text_screens): return self.display_surf

        self.display_surf.fill((255, 255, 255))

        rendered_text_screens: List[pg.Surface] = deepcopy(self.styled_text.rendered_text_screens)

        new_display_surf: pg.Surface = pg.Surface((self.styled_text.wrap_px, self.styled_text.render_height*2))
        new_display_surf.blit(rendered_text_screens[screen_index], (0, 0))
        new_display_surf.blit(rendered_text_screens[screen_index+1], (0, self.styled_text.render_height))

        self.display_surf.blit(new_display_surf, (self.scroll_x, -(self.scroll_y%self.styled_text.render_height)))

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