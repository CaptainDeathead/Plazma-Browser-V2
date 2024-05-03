import pygame as pg
import pygame_gui as pgu
from Ui.elements import H1
from Engine.DOM.document import Document
from Engine.html_parser import HTMLParser

class Renderer:
    def __init__(self, manager: pgu.UIManager):
        self.manager: pgu.UIManager = manager
        self.html_parser: HTMLParser = HTMLParser(self.manager)

    def loadHTML(self, html: str) -> Document:
        return self.html_parser.parseHTML(html)