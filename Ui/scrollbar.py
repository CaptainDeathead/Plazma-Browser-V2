import pygame as pg
from pygame_gui import UIManager
from Ui.button import PGUButton
from config import BUTTON_SCROLL_INCREMENT

class HScrollBar:
    def __init__(self, manager: UIManager, rect: pg.Rect, max_scroll: float, scroll_action: callable) -> None:
        self.manager: UIManager = manager

        self.rect: pg.Rect = rect

        self.x: int = rect.x
        self.y: int = rect.y
        self.width: int = rect.width
        self.height: int = rect.height

        self.scroll: float = 0.0
        self.max_scroll: float = max_scroll

        self.scroll_bar_width: float = self.width - self.height * 2 # buttons size = self.height

        self.bar_x: float = self.scroll * self.scroll_bar_width / self.max_scroll
        self.bar_width: float = self.scroll_bar_width**2 / max_scroll

        self.scroll_bar_bg_rect: pg.Rect = pg.Rect(self.x+self.height, self.y, self.scroll_bar_width, self.height)
        self.scroll_bar_rect: pg.Rect = pg.Rect(self.x+self.height, self.y, self.scroll_bar_width, self.height)

        self.left_button: PGUButton = PGUButton(pg.Rect(self.x, self.y, self.height, self.height), "<", self.manager, lambda: scroll_action(-BUTTON_SCROLL_INCREMENT))
        self.right_button: PGUButton = PGUButton(pg.Rect(self.x+self.width-self.height, self.y, self.height, self.height), ">", self.manager, lambda: scroll_action(BUTTON_SCROLL_INCREMENT))

    def resize(self, new_dimentions: pg.Rect) -> None:
        self.x = new_dimentions.x
        self.y = new_dimentions.y
        self.width = new_dimentions.width
        self.height = new_dimentions.height

        self.scroll_bar_width = self.width - self.height * 2

        self.scroll_bar_bg_rect: pg.Rect = pg.Rect(self.x+self.height, self.y, self.scroll_bar_width, self.height)

        self.recalculate_dimentions()

        self.left_button.set_position((self.x, self.y))
        self.right_button.set_position((self.x+self.width-self.height, self.y))

        self.left_button.set_dimensions((self.height, self.height))
        self.right_button.set_dimensions((self.height, self.height))

    def recalculate_dimentions(self) -> None:
        self.bar_x = (self.scroll_bar_width**2 + self.scroll*self.scroll_bar_width) / self.max_scroll
        self.bar_width = self.scroll_bar_width**2 / self.max_scroll

        self.scroll_bar_rect: pg.Rect = pg.Rect(self.x+self.height+self.bar_x-self.bar_width, self.y, self.bar_width, self.width)

    def set_scroll(self, scroll: float, max_scroll: float = None) -> None:
        self.scroll = scroll

        if max_scroll != None: self.max_scroll = max_scroll

        self.recalculate_dimentions()

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, (100, 100, 100), self.scroll_bar_bg_rect)
        pg.draw.rect(screen, (50, 50, 50), self.scroll_bar_rect, border_radius=5)

class VScrollBar:
    def __init__(self, manager: UIManager, rect: pg.Rect, max_scroll: float, scroll_action: callable) -> None:
        self.manager: UIManager = manager

        self.rect: pg.Rect = rect

        self.x: int = rect.x
        self.y: int = rect.y
        self.width: int = rect.width
        self.height: int = rect.height

        self.scroll: float = 0.0
        self.max_scroll: float = max_scroll

        self.scroll_bar_height: float = self.height - self.width * 2 # buttons size = self.width

        self.bar_y: float = self.scroll * self.scroll_bar_height / self.max_scroll
        self.bar_height: float = self.scroll_bar_height**2 / max_scroll

        self.scroll_bar_bg_rect: pg.Rect = pg.Rect(self.x, self.y+self.width, self.width, self.scroll_bar_height)
        self.scroll_bar_rect: pg.Rect = pg.Rect(self.x, self.y+self.width, self.width, self.scroll_bar_height)

        self.up_button: PGUButton = PGUButton(pg.Rect(self.x, self.y, self.width, self.width), "^", self.manager, lambda: scroll_action(-BUTTON_SCROLL_INCREMENT))
        self.down_button: PGUButton = PGUButton(pg.Rect(self.x, self.y+self.height-self.width, self.width, self.width), "˅", self.manager, lambda: scroll_action(BUTTON_SCROLL_INCREMENT))

    def resize(self, new_dimentions: pg.Rect) -> None:
        self.x = new_dimentions.x
        self.y = new_dimentions.y
        self.width = new_dimentions.width
        self.height = new_dimentions.height

        self.scroll_bar_height = self.height - self.width * 2

        self.scroll_bar_bg_rect: pg.Rect = pg.Rect(self.x, self.y+self.width, self.width, self.scroll_bar_height)
        
        self.recalculate_dimentions()

        self.up_button.set_position((self.x, self.y))
        self.down_button.set_position((self.x, self.y+self.height-self.width))

        self.up_button.set_dimensions((self.width, self.width))
        self.down_button.set_dimensions((self.width, self.width))

    def recalculate_dimentions(self) -> None:
        self.bar_y = (self.scroll_bar_height**2 + self.scroll*self.scroll_bar_height) / self.max_scroll
        self.bar_height = self.scroll_bar_height**2 / self.max_scroll

        self.scroll_bar_rect: pg.Rect = pg.Rect(self.x, self.y+self.width+self.bar_y-self.bar_height, self.width, self.bar_height)

    def set_scroll(self, scroll: float, max_scroll: float = None) -> None:
        self.scroll = scroll

        if max_scroll != None: self.max_scroll = max_scroll

        self.recalculate_dimentions()

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, (100, 100, 100), self.scroll_bar_bg_rect)
        pg.draw.rect(screen, (50, 50, 50), self.scroll_bar_rect, border_radius=5)