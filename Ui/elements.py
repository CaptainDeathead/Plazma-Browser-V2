import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID
from pygame_gui import elements
from typing import Dict, List
from logging import warning

def set_title(relative_rect: pg.Rect = None, manager: pgu.UIManager = None, element_id: str = '', element_class: str = '', options: Dict = {"text": ""}):
    try: pg.display.set_caption(options["text"])
    except: warning("Invalid title!")

class H1(elements.UITextBox):
    def __init__(self, relative_rect: pg.Rect, manager: pgu.UIManager, element_id: str = '', element_class: str = '', options: Dict = {}):
        self.relative_rect: pg.Rect = relative_rect
        self.tag: str = options.get("tag", "h1")
        self.text: str = options.get("text", "").replace('\n', '')
        self.html_str: str = f"<font pixel_size={UI_TEXT_TAG_SIZES[self.tag]}><b>" + options.get("html", "").replace('\n', '') + "</b>"
        self.manager: pgu.UIManager = manager
        super().__init__(self.html_str, relative_rect=self.relative_rect, manager=self.manager)

class H2(elements.UITextBox):
    def __init__(self, relative_rect: pg.Rect, manager: pgu.UIManager, element_id: str = '', element_class: str = '', options: Dict = {}):
        self.relative_rect: pg.Rect = relative_rect
        self.tag: str = options.get("tag", "h2")
        self.text: str = options.get("text", "").replace('\n', '')
        self.html_str: str = f"<font pixel_size={UI_TEXT_TAG_SIZES[self.tag]}><b>" + options.get("html", "").replace('\n', '') + "</b>"
        self.manager: pgu.UIManager = manager
        super().__init__(self.html_str, relative_rect=self.relative_rect, manager=self.manager)

class H3(elements.UITextBox):
    def __init__(self, relative_rect: pg.Rect, manager: pgu.UIManager, element_id: str = '', element_class: str = '', options: Dict = {}):
        self.relative_rect: pg.Rect = relative_rect
        self.tag: str = options.get("tag", "h3")
        self.text: str = options.get("text", "").replace('\n', '')
        self.html_str: str = f"<font pixel_size={UI_TEXT_TAG_SIZES[self.tag]}><b>" + options.get("html", "").replace('\n', '') + "</b>"
        self.manager: pgu.UIManager = manager
        super().__init__(self.html_str, relative_rect=self.relative_rect, manager=self.manager)

class H4(elements.UITextBox):
    def __init__(self, relative_rect: pg.Rect, manager: pgu.UIManager, element_id: str = '', element_class: str = '', options: Dict = {}):
        self.relative_rect: pg.Rect = relative_rect
        self.tag: str = options.get("tag", "h4")
        self.text: str = options.get("text", "").replace('\n', '')
        self.html_str: str = f"<font pixel_size={UI_TEXT_TAG_SIZES[self.tag]}><b>" + options.get("html", "").replace('\n', '') + "</b>"
        self.manager: pgu.UIManager = manager
        super().__init__(self.html_str, relative_rect=self.relative_rect, manager=self.manager)

class H5(elements.UITextBox):
    def __init__(self, relative_rect: pg.Rect, manager: pgu.UIManager, element_id: str = '', element_class: str = '', options: Dict = {}):
        self.relative_rect: pg.Rect = relative_rect
        self.tag: str = options.get("tag", "h5")
        self.text: str = options.get("text", "").replace('\n', '')
        self.html_str: str = f"<font pixel_size={UI_TEXT_TAG_SIZES[self.tag]}><b>" + options.get("html", "").replace('\n', '') + "</b>"
        self.manager: pgu.UIManager = manager
        super().__init__(self.html_str, relative_rect=self.relative_rect, manager=self.manager)

class H6(elements.UITextBox):
    def __init__(self, relative_rect: pg.Rect, manager: pgu.UIManager, element_id: str = '', element_class: str = '', options: Dict = {}):
        self.relative_rect: pg.Rect = relative_rect
        self.tag: str = options.get("tag", "h6")
        self.text: str = options.get("text", "").replace('\n', '')
        self.html_str: str = f"<font pixel_size={UI_TEXT_TAG_SIZES[self.tag]}><b>" + options.get("html", "").replace('\n', '') + "</b>"
        self.manager: pgu.UIManager = manager
        super().__init__(self.html_str, relative_rect=self.relative_rect, manager=self.manager)

class P(elements.UITextBox):
    def __init__(self, relative_rect: pg.Rect, manager: pgu.UIManager, element_id: str = '', element_class: str = '', options: Dict = {}):
        self.relative_rect: pg.Rect = relative_rect
        self.tag: str = options.get("tag", "p")
        self.text: str = options.get("text", "").replace('\n', '')
        self.html_str: str = f"<font pixel_size={UI_TEXT_TAG_SIZES[self.tag]}>" + options.get("html", "").replace('\n', '')
        self.manager: pgu.UIManager = manager
        super().__init__(self.html_str, relative_rect=self.relative_rect, manager=self.manager)
        
class Blank:
    def __init__(self, relative_rect: pg.Rect, manager: pgu.UIManager, element_id: str = '', element_class: str = '', options: Dict = {"text": ""}):
        self.relative_rect: pg.Rect = relative_rect
        self.manager: pgu.UIManager = manager
        
UI_IMPLEMENTED_TAGS: List = ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']
        
UI_ELEMENT_FROM_TAG: Dict = {
    'title': set_title,
    'h1': H1,
    'h2': H2,
    'h3': H3,
    'h4': H4,
    'h5': H5,
    'h6': H6,
    'p': P
}

UI_TEXT_TAG_SIZES: Dict = {
    'h1': 34,
    'h2': 30,
    'h3': 24,
    'h4': 20,
    'h5': 18,
    'h6': 16,
    'p': 16
}

USE_TEXTBOX_TAGS: List = [
    "b", "strong", "i", "em", "var", "u", "br", "p"
]

TEXT_TAGS: List = [
    "h1", "h2", "h3", "h4", "h5", "h6", "p"
]