import pygame as pg
import pygame_gui as pgu
from pygame_gui.core import ObjectID
from pygame_gui import elements
from typing import Dict, List
from logging import warning

def set_title(relative_rect: pg.Rect = None, manager: pgu.UIManager = None, element_id: str = '', element_class: str = '', options: Dict[str, str] = {"text": ""}):
    try: pg.display.set_caption(options["text"])
    except: warning("Invalid title!")
        
UI_IMPLEMENTED_TAGS: List[str] = ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']

UI_TEXT_TAG_SIZES: Dict[str, int] = {
    'h1': 34,
    'h2': 30,
    'h3': 24,
    'h4': 20,
    'h5': 18,
    'h6': 16,
    'p': 16,
    'a': 16
}

UI_DEFAULT_TAG_STYLES: Dict[str, Dict[str, any]] = {
    'h1': {"font-size": UI_TEXT_TAG_SIZES['h1'], "color": "#000000"},
    'h2': {"font-size": UI_TEXT_TAG_SIZES['h2'], "color": "#000000"},
    'h3': {"font-size": UI_TEXT_TAG_SIZES['h3'], "color": "#000000"},
    'h4': {"font-size": UI_TEXT_TAG_SIZES['h4'], "color": "#000000"},
    'h5': {"font-size": UI_TEXT_TAG_SIZES['h5'], "color": "#000000"},
    'h6': {"font-size": UI_TEXT_TAG_SIZES['h6'], "color": "#000000"},
    'p':  {"font-size": UI_TEXT_TAG_SIZES['p' ], "color": "#000000"},
    'a':  {"font-size": UI_TEXT_TAG_SIZES['a' ], "color": "#000000"}
}

USE_TEXTBOX_TAGS: List[str] = [
    "b", "strong", "i", "em", "var", "u", "br"
]

TEXT_TAGS: List[str] = [
    "h1", "h2", "h3", "h4", "h5", "h6", "p"
]

BLOCK_ELEMENTS: List[str] = [
    "address", "article", "aside", "blockquote", "canvas", "dd", "div", "dl", "dt", "fieldset",
    "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr",
    "li", "main", "nav", "noscript", "ol", "p", "pre", "section", "table", "tfoot", "ul", "video"
]