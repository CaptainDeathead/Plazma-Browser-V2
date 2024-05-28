import pygame as pg
import pygame_gui as pgu
from Engine.DOM.document import Document
from Engine.html_parser import HTMLParser
from config import WIN_WIDTH, WIN_HEIGHT, GLOBAL_THEME_PATH
from math import floor
from typing import List
from copy import deepcopy

class Renderer:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.manager: pgu.UIManager = pgu.UIManager((width, height), GLOBAL_THEME_PATH)
        self.html_parser: HTMLParser = HTMLParser(self.manager, width, height)

    def render(self) -> pg.Surface:
        ...

    def loadHTML(self, html: str) -> Document | None:
        self.scroll_x = 0.0
        self.scroll_y = 0.0

        document: Document = self.html_parser.parseHTML(html)

        return document
    
    def loadHTML_NonBlocking(self, html: str, mutable_document_class: Document) -> None:
        # clear the manager
        self.manager: pgu.UIManager = pgu.UIManager((self.width, self.height), GLOBAL_THEME_PATH)
        self.html_parser = HTMLParser(self.manager, self.width, self.height)

        loaded_html: Document | None = self.loadHTML(html)
        
        if loaded_html is not None:
            mutable_document_class = loaded_html