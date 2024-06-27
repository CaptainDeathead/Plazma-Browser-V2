import pygame as pg
from typing import Dict, List, Tuple
from Ui.elements import INLINE_ELEMENTS, TEXT_TAGS, DEFUALT_COLOR
from Engine.Utils.url_utils import resolve_url_in_browser_ctx
from Engine.STR.renderer import StyledText
from config import WIN_WIDTH, WIN_HEIGHT, LINK_NORMAL_COLOR

# IF PYTHON VERSION == 3.11+ UNCOMMENT THIS LINE AND COMMENT OUT THE OTHER ONE
#from typing import Self

# IF PYTHON VERSION < 3.11
from typing_extensions import Self

def darken_color(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return (color[0]//2, color[1]//2, color[2]//2)

class DevtoolsSubElement:
    def __init__(self, rect: pg.Rect, font: pg.Surface) -> None:
        self.rect: pg.Rect = rect
        self.font: pg.Surface = font

        self.selected: bool = False
        self.clicked: bool = False

class Element:
    def __init__(self, tag: str, attributes: Dict, styles: Dict[str, any] = {}, width: int = WIN_WIDTH, height: int = WIN_HEIGHT,
                 parent: Self = None, inline_index: int = 0, depth: int = 0) -> None:
        
        self.tag: str = tag
        self.attributes: Dict = attributes
        self.children: List[Self] = []
        self.parent: Element = parent

        self.htmltype: Dict[str, bool] = self.get_type()

        self.setup_color()

        self.render_function: callable = self.null_render()
        self.update_function: callable = self.null_update()

        self.inline_index: int = inline_index
        self.depth: int = depth

        # surface and render attributes
        self.max_width: int = width
        self.max_height: int = height

        self.devtools_attrs: DevtoolsSubElement = None
        
        self.rect: pg.Rect = pg.Rect(0, 0, 0, 0)
        self.rect_unused: pg.Rect = pg.Rect(0, 0, 0, 0)
        
        self.hovered: bool = False
        self.pressed: bool = False
        self.clicked: bool = False

        self.isinline: bool = self.tag in INLINE_ELEMENTS

        self.styles: Dict[str, any] = styles

        self.scroll_x: float = 0.0
        self.scroll_y: float = 0.0

        self.reload_required: bool = False
        self.page_reload_required: bool = False
        self.style_overides: Dict[str, any] = {}

        self.url_redirect: str = ""

        self.get_render_function()
        self.get_update_function()

    def get_type(self) -> Dict[str, bool]:
        htmltype: Dict[str, bool] = {
            "text": False,
            "link": False
        }

        if self.tag in TEXT_TAGS: htmltype["text"] = True
        if self.tag == "a": htmltype["link"] = True

        return htmltype
    
    def setup_color(self) -> None:
        self.color: Tuple[int, int, int] = self.attributes.get("color", None)

        self.LINK_NORMAL_COLOR: Tuple[int, int, int] = self.attributes.get("color", LINK_NORMAL_COLOR)
        self.PRESSED_LINK_COLOR: Tuple[int, int, int] = self.attributes.get("plazma_browser_hovered_color", darken_color(self.LINK_NORMAL_COLOR))

        if self.color == None:
            if self.htmltype["link"]: self.color = self.LINK_NORMAL_COLOR
            else: self.color = DEFUALT_COLOR

    def get_render_function(self) -> None:
        if self.htmltype["text"]: self.render_function = self.render_text
        else: self.update_function = self.null_render

    def get_update_function(self) -> None:
        if self.htmltype["link"]: self.update_function = self.update_link
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

    def null_render(self, *args, **kwargs) -> None:
        return None
    
    def render_text(self, styled_text: StyledText, x: int, y: int) -> None:
        text: str = self.attributes.get("text")
        font: Tuple[str, int] = (self.styles["font-name"], self.styles["font-size"])
        font_type: Tuple[bool, bool, bool] = (self.styles["bold"], self.styles["italic"], self.styles["underline"])
        color: Tuple[int, int, int] = self.color
        bg_color: Tuple[int, int, int] = self.styles["background-color"]
        ...
        padding_y: int = 2

        self.rect, self.rect_unused = styled_text.renderStyledText(text, font, font_type, color, bg_color, x, y, self.max_width, self.max_height, padding_y)

    def render(self, styled_text: StyledText, x: int, y: int) -> None:
        # TODO: Make render function here
        self.render_function(styled_text, x, y)

    def update(self) -> Tuple[bool, bool]:
        self.update_function()

        return (self.reload_required, self.page_reload_required)

    def update_link(self) -> None:
        if self.clicked:
            url: str = self.attributes.get("href", "#")
            full_url: str = resolve_url_in_browser_ctx(url)

            if full_url != "#":
                self.page_reload_required = True
                self.url_redirect = full_url

            self.clicked = False

        if self.pressed:
            if self.color != self.PRESSED_LINK_COLOR:
                self.style_overides["color"] = self.PRESSED_LINK_COLOR
                self.reload_required = True
        else:
            if self.color != self.LINK_NORMAL_COLOR:
                self.style_overides["color"] = self.LINK_NORMAL_COLOR
                self.reload_required = True

    def null_update(self) -> None:
        return