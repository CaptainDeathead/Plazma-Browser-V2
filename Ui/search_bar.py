import pygame as pg
import pygame_gui as pgu

class SearchBar(pgu.elements.UITextEntryLine):
    def __init__(self, relative_rect: pg.Rect, manager: pgu.UIManager):
        super().__init__(relative_rect=relative_rect, manager=manager)