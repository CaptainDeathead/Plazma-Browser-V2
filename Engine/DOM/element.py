import pygame as pg
from typing import Dict, List
from config import WIN_WIDTH, WIN_HEIGHT

class Element:
    def __init__(self, tag: str, attributes: Dict, rect: pg.Rect = None, rect_unused: pg.Rect = None, styles: Dict[str, any] = {},
                 width: int = WIN_WIDTH, height: int = WIN_HEIGHT) -> None:
        self.tag: str = tag
        self.attributes: Dict = attributes
        self.children: List = []

        # surface and render attributes
        self.max_width: int = width
        self.max_height: int = height
        
        self.rect: pg.Rect = rect
        self.rect_unused: pg.Rect = rect_unused
        
        self.hovered: bool = False
        #self.clickable: bool = is_clickable(self.tag)
        self.clicked: bool = False

        self.styles: Dict[str, any] = styles

        self.scroll_x: float = 0.0
        self.scroll_y: float = 0.0