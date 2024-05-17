from typing import Dict, List
from Ui.elements import *

def is_clickable(tag: str) -> bool:
    if tag in ("a", "button"):
        return True
    else:
        return False

class Element:
    def __init__(self, tag: str, attributes: Dict, rect: pg.Rect = None, styles: Dict[str, any] = {}) -> None:
        self.tag: str = tag
        self.attributes: Dict = attributes
        self.children: List = []

        # surface and render attributes
        self.rect: pg.Rect = rect
        
        self.hovered: bool = False
        self.clickable: bool = is_clickable(self.tag)
        self.clicked: bool = False

        self.styles: Dict[str, any] = styles