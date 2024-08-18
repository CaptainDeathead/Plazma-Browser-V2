import pygame as pg
import pygame_gui as pgu
from typing import Dict, List, Tuple
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

DEFAULT_COLOR: Tuple[int, int, int] = (0, 0, 0)
DEFAULT_BG_COLOR: Tuple[int, int, int] = (255, 255, 255)
DEFAULT_FONT: Tuple[str, int] = ("arial", 18)
DEFAULT_PADDING: Tuple[int, int, int, int] = (2, 0, 0, 10) # 0: top, 1: right, 2: bottom, 3: left

DEFAULT_STYLES: Dict[str, any] = {
    'color': DEFAULT_COLOR,
    'background-color': DEFAULT_BG_COLOR,
    'font-name': DEFAULT_FONT[0],
    'font-size': DEFAULT_FONT[1],
    'padding': DEFAULT_PADDING, # 0: top, 1: right, 2: bottom, 3: left

    'bold': False,
    'italic': False,
    'underline': False,

    'link': False
}