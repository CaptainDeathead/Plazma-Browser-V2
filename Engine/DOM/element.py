import pygame as pg
from pygame_gui.elements import UIScrollingContainer
from typing import Dict, List
from config import WIN_WIDTH, WIN_HEIGHT

class Element:
    def __init__(self, tag: str, attributes: Dict, styles: Dict[str, any], container: UIScrollingContainer) -> None:
        
        self.tag: str = tag
        self.attributes: Dict = attributes
        self.children: List = []

        self.styles: Dict[str, any] = styles

        self.container: UIScrollingContainer = container