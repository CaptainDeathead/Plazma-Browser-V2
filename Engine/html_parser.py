import pygame as pg
import logging
import cssutils
from cssutils import parseString
from cssutils.css import CSSStyleSheet
from Engine.DOM.document import Document
from Engine.DOM.element import Element
from Engine.themes import ThemeManager
from typing import Dict, Tuple
from bs4 import BeautifulSoup, element
from pygame_gui import UIManager
from pygame_gui.core import ObjectID
from pygame_gui.elements import UILabel, UIButton, UIScrollingContainer
from Ui.elements import UI_TEXT_TAG_SIZES, UI_DEFAULT_TAG_STYLES, TEXT_TAGS, USE_TEXTBOX_TAGS, BLOCK_ELEMENTS
from pygame.display import set_caption
from re import finditer
from copy import deepcopy
from config import GLOBAL_THEME_PATH

cssutils.log.setLevel(logging.CRITICAL)

def find_nums(string_with_nums: str) -> Tuple[float, str] | None:
    for i in range(len(string_with_nums)):
        if string_with_nums[i].isalpha() or string_with_nums[i] == '%':
            return float(string_with_nums[:i]), string_with_nums[i:]

    return None

def remove_units(num_str: str, tag_size: float, parent_size: float, view_width: float, view_height: float) -> float:
    num_str = num_str.lower()

    split_num: Tuple[float, str] | None = find_nums(num_str)

    if split_num is None: return float(num_str)
    
    value, unit = split_num
    
    if unit == "cm": return value * 37.8
    elif unit == "mm": return value * 3.78
    elif unit == "q": return value * 0.945
    elif unit == "in": return value * 96
    elif unit == "pc": return value * 16
    elif unit == "pt": return value * 1.333333
    elif unit == "px": return value

    # relative sizes
    elif unit == "em": return value * parent_size
    elif unit == "rem": return value * tag_size
    elif unit == "vw": return view_width / value
    elif unit == "vh": return view_height / value
    elif unit == "%": return tag_size * value / 100
    
    return float(num_str)

class HTMLParser:
    def __init__(self, manager: UIManager, width: int, height: int) -> None:
        self.document: Document = Document()
        self.manager: UIManager = manager
        self.theme_manager: ThemeManager = ThemeManager()
        self.curr_x: float = 0.0
        self.curr_y: float = 0.0
        self.largest_y: float = 0.0
        self.stop_loading: bool = False

        self.container_width: int = width
        self.container_height: int = height

        # config the global theme file that the theme_manager has access to
        self.manager.create_new_theme(GLOBAL_THEME_PATH)

        self.curr_machine_theme: int = 0

    def feed_line(self) -> None:
        self.curr_x = 0.0
        self.curr_y += self.largest_y
        self.largest_y = 0.0

    def recurse_tag_children(self, tag: element.Tag, parent_element: Element) -> None:
        if self.stop_loading: return
        
        for child_tag in tag.children:
            if isinstance(child_tag, element.Tag):
                child_tag.attrs["tag"] = child_tag.name
                child_tag.attrs["text"] = child_tag.text.replace('\n', '')
                child_tag.attrs["html"] = str(child_tag).replace('\n', '')

                # head tags
                if child_tag.name == "title": set_caption(f"Plazma Browser (Dev) | {child_tag.attrs['text']}")

                text_rect: pg.Rect = None
                text_rect_unused: pg.Rect = None

                # inherit parent styles
                tag_styles: Dict[str, any] = deepcopy(parent_element.styles)

                # add styles for text info when sizing fonts
                tag_styles["text-tag-size"] = UI_TEXT_TAG_SIZES.get(child_tag.name, 16)
                tag_styles["parent-tag-size"] = parent_element.styles.get("text-tag-size", 16)

                if child_tag.name == 'i': tag_styles["italic"] = True
                elif child_tag.name == 'b' or child_tag.name == 'strong': tag_styles["bold"] = True
                elif child_tag.name == 'u': tag_styles["underline"] = True
                elif child_tag.name == 'br':
                    self.feed_line()

                element_width: int = int(remove_units(str(child_tag.attrs.get("width", 0)), 0, 0, self.container_width, self.container_height))
                element_height: int = int(remove_units(str(child_tag.attrs.get("height", 0)), 0, 0, self.container_width, self.container_height))

                # ---------- PRE-PARSING ----------

                child_tag_html: str = child_tag.attrs["html"]

                if child_tag.name in TEXT_TAGS and child_tag.text != "":
                    if '<browser_text>' not in child_tag.attrs["html"]:
                        open_tags = [tag.start() for tag in finditer('<', child_tag_html)]
                        close_tags = [tag.start() for tag in finditer('>', child_tag_html)]

                        tag_offset: int = 0
        
                        for i in range(0, len(close_tags)-1, 1):
                            if child_tag_html[close_tags[i]+tag_offset+1] != '<':
                                # <browser_text> has a length of 14
                                child_tag.attrs["html"] = "{}{}{}".format(child_tag_html[:close_tags[i]+tag_offset+1], "<browser_text>", child_tag_html[close_tags[i]+tag_offset+1:])
                                child_tag_html = child_tag.attrs["html"]
                                tag_offset += 14
                                
                                child_tag.attrs["html"] = "{}{}{}".format(child_tag_html[:open_tags[i+1]+tag_offset], "</browser_text>", child_tag_html[open_tags[i+1]+tag_offset:])
                                child_tag_html = child_tag.attrs["html"]
                                tag_offset += 15

                        # reload child tag with formatted html_text
                        child_tag = BeautifulSoup(child_tag_html, 'html.parser')

                        child_tag.attrs["tag"] = child_tag.name
                        child_tag.attrs["text"] = child_tag.text.replace('\n', '')
                        child_tag.attrs["html"] = str(child_tag).replace('\n', '')

                    else:
                        tag_styles['font-size'] = str(UI_TEXT_TAG_SIZES.get(child_tag.name, 16)) + "px"

                # ---------- PARSING ----------

                if "style" in child_tag.attrs:
                    styles = child_tag.attrs["style"]

                    sheet: CSSStyleSheet = parseString(child_tag.name + "{ " + styles + " }")
                    
                    for rule in sheet:
                        for property in rule.style:
                            if property.name == 'font-family':
                                tag_styles['font'] = property.value.split(',')[0]
                            else:
                                tag_styles[property.name] = property.value

                # add default styles if needed
                if child_tag.name in UI_DEFAULT_TAG_STYLES:
                    default_tag_styles = deepcopy(UI_DEFAULT_TAG_STYLES[child_tag.name])

                    default_tag_styles.update(tag_styles)

                    tag_styles = default_tag_styles

                if child_tag.name == 'browser_text':

                    # applying theme
                    tag_id: int | None = child_tag.attrs.get("id", None)

                    if tag_id is None:
                        tag_id = self.curr_machine_theme
                        self.curr_machine_theme += 1
                    else:
                        tag_styles = self.theme_manager.mergeStyles(tag_styles, tag_id)
                    
                    tag_id = self.theme_manager.generateTheme(tag_id, tag_styles)

                    text_label: UILabel = UILabel(pg.Rect(self.curr_x, self.curr_y, -1, -1), child_tag.attrs["text"], self.manager, parent_element.container, object_id=ObjectID(object_id=tag_id))

                    text_label_rect: pg.Rect = text_label.get_abs_rect()

                    self.curr_x += text_label_rect.width

                    if text_label_rect.height > self.largest_y:
                        self.largest_y = text_label_rect.height

                    parent_element.children.append(Element(child_tag.name, child_tag.attrs, tag_styles, parent_element.container))
                else:
                    if child_tag.name in BLOCK_ELEMENTS: self.feed_line()

                    parent_element.children.append(Element(child_tag.name, child_tag.attrs, tag_styles, parent_element.container))

                self.recurse_tag_children(child_tag, parent_element.children[-1])
        
    def parseHTML(self, html: str, thread_id: int = 0) -> Document | None:
        soup = BeautifulSoup(html, 'html.parser')

        first_elem = soup.find()

        body_container: UIScrollingContainer = UIScrollingContainer(pg.Rect(0, 0, self.container_width, self.container_height), self.manager)
        body_container.set_scrollable_area_dimensions((self.container_width, self.container_height))

        self.document.html_element = Element(first_elem.name, first_elem.attrs, {}, body_container)

        self.document.html_element.styles["view-width"] = self.container_width
        self.document.html_element.styles["view-height"] = self.container_height

        self.recurse_tag_children(first_elem, self.document.html_element)
        if self.stop_loading: return None

        logging.debug("Finished parsing html!")

        return self.document