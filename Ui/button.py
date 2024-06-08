import pygame as pg
from pygame_gui import UIManager
from pygame_gui.elements import UIButton
from typing import Dict, List, Tuple
from exceptions import StyleNotIncludedException
from copy import deepcopy

class PGUButton(UIButton):
    def __init__(self, rect: pg.Rect, text: str, manager: UIManager, click_action: callable) -> None:
        super().__init__(rect, text, manager=manager)

        self.click_action: callable = click_action

class Button(pg.Rect):
    BASE_STYLES: Dict[str, any] = {
        "border-radius": 0
    }

    REQUIRED_STYLES: List[str] = ["color", "background-color"]

    def __init__(self, rect: pg.Rect, text: str, font: pg.Font, styles: Dict[str, any]) -> None:
        super().__init__(rect.x, rect.y, rect.width, rect.height)
        
        self._check_styles(styles)

        self.styles: Dict[str, any] = deepcopy(self.BASE_STYLES)

        self.styles.update(styles)

        self.text: str = text
        self.font: pg.Font = font

    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, self.styles["background-color"], pg.Rect(self.x, self.y, self.width, self.height), border_radius=self.styles["border-radius"])

        font_surface: pg.Surface = self.font.render(self.text, True, self.styles["color"])

        screen.blit(font_surface, (self.x + self.width/2-font_surface.get_width()/2, self.y + self.height/2-font_surface.get_height()/2))

    def _check_styles(self, styles) -> None:
        for style in self.REQUIRED_STYLES:
            if style not in styles:
                raise StyleNotIncludedException(style, self.REQUIRED_STYLES, Button)