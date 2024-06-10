import pygame as pg
from typing import Dict, List
from Ui.elements import INLINE_ELEMENTS
from config import WIN_WIDTH, WIN_HEIGHT, LINK_NORMAL_COLOR, PRESSED_LINK_COLOR

# IF PYTHON VERSION == 3.11+ UNCOMMENT THIS LINE AND COMMENT OUT THE OTHER ONE
#from typing import Self

# IF PYTHON VERSION < 3.11
from typing_extensions import Self

class Element:
    def __init__(self, tag: str, attributes: Dict, rect: pg.Rect, rect_unused: pg.Rect, styles: Dict[str, any] = {},
                 width: int = WIN_WIDTH, height: int = WIN_HEIGHT, parent: Self = None, inline_index: int = 0,
                 depth: int = 0) -> None:
        
        self.tag: str = tag
        self.attributes: Dict = attributes
        self.children: List = []
        self.parent: Element = parent

        self.update_function: callable = self.null_update()

        self.inline_index: int = inline_index
        self.depth: int = depth

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

        self.reload_required: bool = False
        self.style_overides: Dict[str, any] = {}

        self.get_update_function()

    def get_update_function(self) -> None:
        if self.tag == "a": self.update_function = self.update_link
        else: self.update_function = self.null_update

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

    def add_status(self, status: Dict[str, any]) -> None:
        for key in status:
            if key == "hovered": self.hovered = status[key]
            elif key == "pressed": self.pressed = status[key]

    def update(self) -> None:
        self.update_function()

        return self.reload_required

    def update_link(self) -> None:
        #print(self.hovered, self.pressed)
        if self.pressed:
            if self.styles["color"] != PRESSED_LINK_COLOR:
                self.style_overides["color"] = PRESSED_LINK_COLOR
                self.reload_required = True
        else:
            if self.styles["color"] != LINK_NORMAL_COLOR:
                self.style_overides["color"] = LINK_NORMAL_COLOR
                self.reload_required = True

    def null_update(self) -> None:
        return