import pygame as pg
from typing import Dict, List
from Ui.elements import INLINE_ELEMENTS
from config import WIN_WIDTH, WIN_HEIGHT

# IF PYTHON VERSION == 3.11+ UNCOMMENT THIS LINE AND COMMENT OUT THE OTHER ONE
#from typing import Self

# IF PYTHON VERSION < 3.11
from typing_extensions import Self

class Element:
    def __init__(self, tag: str, attributes: Dict, rect: pg.Rect, rect_unused: pg.Rect, styles: Dict[str, any] = {},
                 width: int = WIN_WIDTH, height: int = WIN_HEIGHT, parent: Self = None, inline_index: int = 0) -> None:
        
        self.tag: str = tag
        self.attributes: Dict = attributes
        self.children: List = []
        self.parent: Element = parent

        self.inline_index: int = inline_index

        # surface and render attributes
        self.max_width: int = width
        self.max_height: int = height
        
        self.rect: pg.Rect = rect
        self.rect_unused: pg.Rect = rect_unused
        
        self.hovered: bool = False
        self.pressed: bool = False

        self.styles: Dict[str, any] = styles

        self.scroll_x: float = 0.0
        self.scroll_y: float = 0.0

    def resize_family_rects(self, parent: Self) -> None:
        if parent is None: return

        if parent.rect.x == 0: parent.rect.x = self.rect.x
        if parent.rect.y == 0: parent.rect.y = self.rect.y

        local_x: int = self.rect.x - parent.rect.x
        local_y: int = self.rect.y - parent.rect.y

        largest_width: int = local_x + self.rect.width
        largest_height: int = local_y + self.rect.height

        if self.inline_index > 0:
            parent.rect.width += self.rect.width

            if largest_height > parent.rect.height: parent.rect.height = largest_height
        else:
            if largest_width > parent.rect.width: parent.rect.width = largest_width

            parent.rect.height += self.rect.height

    def update(self) -> None:
        ...