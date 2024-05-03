import pygame as pg
import pygame_gui as pgu
from Ui.elements import H1
from Engine.DOM.document import Document
from Engine.html_parser import HTMLParser
from Engine.STR.renderer import StyledText
from config import WIDTH, HEIGHT

class Renderer:
    def __init__(self, manager: pgu.UIManager):
        self.manager: pgu.UIManager = manager
        self.styled_text: StyledText = StyledText("\n", WIDTH, HEIGHT, (0, 0, 0), (255, 255, 255), "Calibri", 16, (2, 5, 2, 5))
        self.html_parser: HTMLParser = HTMLParser(self.manager)

    def loadHTML(self, html: str) -> Document:
        return self.html_parser.parseHTML(html)