import pygame as pg
import pygame_gui as pgu
from Engine.DOM.document import Document
from Engine.DOM.element import Element
from Engine.html_parser import HTMLParser
from Engine.STR.renderer import StyledText
from typing import List, Tuple
from config import SHOW_ALL_SURFACE_CONTAINERS

class Renderer:
    def __init__(self, manager: pgu.UIManager, width: int, height: int, load_page: callable):
        self.manager: pgu.UIManager = manager
        self.styled_text: StyledText = StyledText("\n", width, height, (0, 0, 0), (255, 255, 255), "Arial", 16, (2, 20, 2, 20))
        self.html_parser: HTMLParser = HTMLParser(self.manager, self.styled_text, width, height)
        self.display_surf: pg.Surface = pg.Surface((width, height))
        self.dev_tools_surface: pg.Surface = pg.Surface((width, height), pg.SRCALPHA, 32)
        self.load_page: callable = load_page

        self.width: int = width
        self.height: int = height

        self.scroll_x: float = 0.0
        self.scroll_y: float = 0.0

        self.mouse_pos: Tuple[int, int] = pg.mouse.get_pos()
        
        self.lmb_pressed_last_frame: bool = False
        self.lmb_pressed: bool = pg.mouse.get_pressed()[0]

        self.mouse_type: int = pg.SYSTEM_CURSOR_ARROW

    def move_scroll_x(self, scroll_x: float) -> None:
        self.scroll_x += scroll_x
        self.scroll_x = max(min(self.scroll_x, self.styled_text.rendered_text.get_width()-self.width), 0)

    def move_scroll_y(self, scroll_y: float) -> None:
        self.scroll_y += scroll_y
        self.scroll_y = max(min(self.scroll_y, self.styled_text.rendered_text.get_height()-self.height), 0)

    def render(self) -> pg.Surface:
        self.update_elements()

        self.display_surf: pg.Surface = pg.Surface((self.width, self.height))
        self.display_surf.blit(self.styled_text.rendered_text, (-self.scroll_x, -self.scroll_y))

        self.display_surf.blit(self.dev_tools_surface.convert_alpha(), (0, 0))

        return self.display_surf
    
    def resize(self, width: int, height: int) -> None:
        self.width, self.height = width, height

        self.dev_tools_surface = pg.Surface((self.width, self.height), pg.SRCALPHA, 32)
    
    def remove_mouse_status(self, element: Element) -> None:
        element.hovered = False
        element.pressed = False

    def reload_element(self, element: Element) -> None:
        element.reload_required = False
        
        self.html_parser.reparse_element(element, element.style_overides)

    def reset_devtools(self) -> None:
        self.dev_tools_surface = pg.Surface((self.width, self.height), pg.SRCALPHA, 32)

    def update_element(self, element: Element) -> bool:
        hand_cursor = False

        if element.rect.collidepoint(self.mouse_pos):
            if not element.rect_unused.collidepoint(self.mouse_pos):                
                if not element.hovered: element.hovered = True

                if self.lmb_pressed:
                    if not element.pressed:
                        element.pressed = True
                else:
                    if element.pressed: element.clicked = True

                    element.pressed = False

                if element.tag == "a": hand_cursor = True

            else:
                self.remove_mouse_status(element)
        else:
            self.remove_mouse_status(element)

        reload_required, page_reload_required = element.update()

        if page_reload_required: self.load_page(element.url_redirect)
        elif reload_required: self.reload_element(element)

        if SHOW_ALL_SURFACE_CONTAINERS:
            dev_surface: pg.Surface = pg.Surface((element.rect.width, element.rect.height), pg.SRCALPHA)
            dev_surface.set_alpha(int(element.depth*4))
            dev_surface.fill((255, 0, 255))
            self.dev_tools_surface.blit(dev_surface, (element.rect.x - self.scroll_x, element.rect.y - self.scroll_y))

        return hand_cursor

    def search_children_iterative_preoder_traversal(self, element: Element) -> bool:
        if element == None: return False

        root: Element = element

        hand_cursor: bool = False

        nodeStack: List[Element] = []
        nodeStack.append(root)

        while len(nodeStack) > 0:
            node = nodeStack.pop()

            new_hand_cursor: Element = self.update_element(node)

            if new_hand_cursor == True: hand_cursor = new_hand_cursor

            # only update children if parent is hovered
            if node.hovered:
                for childNode in node.children:
                    nodeStack.append(childNode)

        return hand_cursor

    def update_elements(self) -> None:
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_pos = (self.mouse_pos[0]+self.scroll_x, self.mouse_pos[1]+self.scroll_y-50)

        self.lmb_pressed = pg.mouse.get_pressed()[0]

        self.reset_devtools()

        hand_cursor: bool = self.search_children_iterative_preoder_traversal(self.html_parser.document.html_element)

        if hand_cursor:
            if self.mouse_type != pg.SYSTEM_CURSOR_HAND: self.mouse_type = pg.SYSTEM_CURSOR_HAND

        else: self.mouse_type = pg.SYSTEM_CURSOR_ARROW
        
        pg.mouse.set_cursor(self.mouse_type)

    def loadHTML(self, html: str) -> Document | None:
        self.scroll_x = 0.0
        self.scroll_y = 0.0
        
        # clear text
        self.styled_text.clear()

        document: Document = self.html_parser.parseHTML(html)

        return document
    
    def loadHTML_NonBlocking(self, html: str, mutable_document_class: Document) -> None:
        loaded_html: Document | None = self.loadHTML(html)
        
        if loaded_html is not None:
            mutable_document_class = loaded_html