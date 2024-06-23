import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID
from pygame_gui import elements
from typing import Dict, List
from logging import warning

def set_title(relative_rect: pg.Rect = None, manager: pgu.UIManager = None, element_id: str = '', element_class: str = '', options: Dict = {"text": ""}):
    try: pg.display.set_caption(options["text"])
    except: warning("Invalid title!")
        
DEFAULT_START_RENDER_X: float = 10.0

DEFAULT_BLOCK_SPACING_Y: float = 20.0

UI_IMPLEMENTED_TAGS: List = ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']

UI_TEXT_TAG_SIZES: Dict = {
    'h1': 34,
    'h2': 30,
    'h3': 24,
    'h4': 20,
    'h5': 18,
    'h6': 16,
    'p': 16,
    'a': 16
}

USE_TEXTBOX_TAGS: List = [
    "b", "strong", "i", "em", "var", "u", "br"
]

TEXT_TAGS: List = [
    "h1", "h2", "h3", "h4", "h5", "h6", "p"
]

INLINE_ELEMENTS: List[str] = ["a", "abbr", "acronym", "b", "bdo", "big", "br", "button", "cite",
                              "code", "dfn", "em", "i", "img", "input", "kbd", "label", "map",
                              "object", "output", "q", "samp", "script", "select", "small", "span",
                              "strong", "sub", "sup", "textarea", "time", "tt", "var", "browser_text"]