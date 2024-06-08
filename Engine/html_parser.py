import pygame as pg
import logging
import cssutils
from cssutils import parseString
from cssutils.css import CSSStyleSheet
from Engine.DOM.document import Document
from Engine.DOM.element import Element
from typing import Dict, Tuple
from bs4 import BeautifulSoup, element
from pygame_gui import UIManager
from Ui.elements import UI_TEXT_TAG_SIZES, TEXT_TAGS, USE_TEXTBOX_TAGS, INLINE_ELEMENTS
from Engine.STR.renderer import StyledText, remove_units, ishex, hex_to_rgb
from pygame.display import set_caption
from re import finditer
from copy import deepcopy
from config import SHOW_PRIMARY_SURFACE_CONTAINERS, LINK_NORMAL_COLOR, PRESSED_LINK_COLOR, BASE_TITLE

cssutils.log.setLevel(logging.CRITICAL)

def containsnum(string: str) -> bool:
    for i in range(10):
        if str(i) in string: return True

    return False

class HTMLParser:
    EMPTY_RECT: pg.Rect = pg.Rect(0, 0, 0, 0)

    def __init__(self, manager: UIManager, styled_text: StyledText, width: int, height: int) -> None:
        self.document: Document = Document()
        self.manager: UIManager = manager
        self.styled_text: StyledText = styled_text
        self.curr_y: int = 0
        self.stop_loading: bool = False

        self.container_width: int = width
        self.container_height: int = height

    def recurse_tag_children(self, tag: element.Tag, parent_element: Element, inline_elements: int = 0, depth: int = 0) -> None:
        if self.stop_loading: return
        
        for child_tag in tag.children:
            if isinstance(child_tag, element.Tag):
                if child_tag.name in INLINE_ELEMENTS: inline_elements += 1

                child_tag.attrs["tag"] = child_tag.name
                child_tag.attrs["text"] = child_tag.text.replace('\n', '')
                child_tag.attrs["html"] = str(child_tag).replace('\n', '')

                # head tags
                if child_tag.name == "title": set_caption(BASE_TITLE + child_tag.attrs['text'])

                text_rect: pg.Rect = parent_element.rect
                text_rect_unused: pg.Rect = parent_element.rect_unused

                # inherit parent styles
                tag_styles: Dict[str, any] = deepcopy(parent_element.styles)

                # add styles for text info when sizing fonts
                tag_styles["text-tag-size"] = UI_TEXT_TAG_SIZES.get(child_tag.name, 16)
                tag_styles["parent-tag-size"] = parent_element.styles.get("text-tag-size", 16)

                if child_tag.name == 'i': tag_styles["italic"] = True
                elif child_tag.name == 'b' or child_tag.name == 'strong': tag_styles["bold"] = True
                elif child_tag.name == 'u': tag_styles["underline"] = True
                elif child_tag.name == 'br':
                    if parent_element is not None and type(parent_element.rect) == pg.Rect:
                        parent_element.rect.height += self.styled_text.renderStyledText('\n')[0].height
                    else:
                        self.styled_text.renderStyledText('\n')[0].height

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

                        # feed line because its a block element
                        if parent_element is not None and type(parent_element.rect) == pg.Rect:
                            parent_element.rect.height += self.styled_text.renderStyledText('\n')[0].height
                        else:
                            self.styled_text.renderStyledText('\n')[0].height
                    else:
                        tag_styles['font-size'] = UI_TEXT_TAG_SIZES.get(child_tag.name, 16)

                # ---------- PARSING ----------

                if "style" in child_tag.attrs:
                    styles = child_tag.attrs["style"]

                    sheet: CSSStyleSheet = parseString(child_tag.name + "{ " + styles + " }")
                    
                    for rule in sheet:
                        for property in rule.style:
                            if property.name == 'font-family':
                                tag_styles['font'] = property.value.split(',')[0]
                            else:
                                value: str | float | int = property.value

                                if type(value) == str:
                                    if ishex(value): value = hex_to_rgb(value)

                                    elif containsnum(value):
                                        value = remove_units(value, tag_styles["font-size"], parent_element.styles["font-size"],
                                                            self.container_width, self.container_height)
                                    
                                tag_styles[property.name] = value

                element_width: int = int(remove_units(str(child_tag.attrs.get("width", tag_styles.get("width", 0))),
                                                      tag_styles["font-size"], parent_element.styles["font-size"],
                                                      self.container_width, self.container_height))
                
                element_height: int = int(remove_units(str(child_tag.attrs.get("height", tag_styles.get("height", 0))),
                                                       tag_styles["font-size"], parent_element.styles["font-size"],
                                                       self.container_width, self.container_height))

                if child_tag.name == 'browser_text':
                    text_rect, text_rect_unused = self.styled_text.renderStyledText(f"{child_tag.attrs['text']}", tag_styles)

                    if SHOW_PRIMARY_SURFACE_CONTAINERS:
                        text_rect_dev_surface: pg.Surface = pg.Surface((text_rect.width, text_rect.height))
                        text_rect_dev_surface.set_alpha(int(128))
                        text_rect_dev_surface.fill((255, 0, 0))
                        self.styled_text.rendered_text.blit(text_rect_dev_surface, (text_rect.x, text_rect.y))

                        text_rect_unused_dev_surface: pg.Surface = pg.Surface((text_rect_unused.width, text_rect_unused.height))
                        text_rect_unused_dev_surface.set_alpha(int(128))
                        text_rect_unused_dev_surface.fill((0, 255, 0))
                        self.styled_text.rendered_text.blit(text_rect_unused_dev_surface, (text_rect_unused.x, text_rect_unused.y))

                    new_element: Element = Element(child_tag.name, child_tag.attrs, text_rect, text_rect_unused,
                                                        tag_styles, element_width, element_height, parent_element,
                                                        inline_elements)
                else:
                    if child_tag.name == 'a':
                        tag_styles["color"] = LINK_NORMAL_COLOR

                    new_element: Element = Element(child_tag.name, child_tag.attrs, self.EMPTY_RECT, self.EMPTY_RECT,
                                                        tag_styles, element_width, element_height, parent_element,
                                                        inline_elements)
                    
                if new_element.rect != self.EMPTY_RECT:
                    new_element.resize_family_rects(new_element.parent)

                parent_element.children.append(new_element)

                self.recurse_tag_children(child_tag, parent_element.children[-1], inline_elements, depth + 1)
        
    def parseHTML(self, html: str, thread_id: int = 0) -> Document | None:
        html = "<plazma-browser>" + html + "</plazma-browser>"

        soup = BeautifulSoup(html, 'html.parser')

        first_elem = soup.find()

        self.document.html_element = Element(first_elem.name, first_elem.attrs, self.EMPTY_RECT, self.EMPTY_RECT)

        self.document.html_element.styles["view-width"] = self.container_width
        self.document.html_element.styles["view-height"] = self.container_height

        self.document.html_element.styles['font-size'] = 16

        self.recurse_tag_children(first_elem, self.document.html_element)
        if self.stop_loading: return None

        logging.debug("Finished parsing html!")

        return self.document