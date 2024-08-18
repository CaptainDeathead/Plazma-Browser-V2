import pygame as pg
import logging
from pygame.display import set_caption
from bs4 import BeautifulSoup, element
from Engine.DOM.document import Document
from Engine.DOM.element import Element
from Engine.STR.renderer import StyledText, feed_line
from Engine.css_parser import CSSParser
from pygame_gui import UIManager
from Ui.elements import UI_TEXT_TAG_SIZES, TEXT_TAGS, USE_TEXTBOX_TAGS, INLINE_ELEMENTS
from re import finditer
from copy import deepcopy
from typing import Dict, List, Tuple
from Engine.Utils.utils import remove_units
from config import SHOW_PRIMARY_SURFACE_CONTAINERS, BASE_TITLE

class HTMLParser:
    EMPTY_RECT: pg.Rect = pg.Rect(0, 0, 0, 0)

    def __init__(self, manager: UIManager, styled_text: StyledText, css_parser: CSSParser, width: int, height: int) -> None:
        self.document: Document = Document()
        self.manager: UIManager = manager
        self.styled_text: StyledText = styled_text
        self.css_parser: CSSParser = css_parser

        self.curr_y: int = 0

        self.stop_loading: bool = False

        self.container_width: int = width
        self.container_height: int = height

    def find_closest_container(self, element: Element) -> Element | None:
        if element is None: return element
        elif not element.istext: return element

        nodeStack: List[Element] = []
        nodeStack.append(element)

        while len(nodeStack) > 0:
            node = nodeStack.pop()

            if not node.istext: return node
            else: nodeStack.append(node.parent)

        return element
    
    def populateElementTree(self, tag: element.Tag, parent_element: Element) -> None:

        nodeStack: List[Tuple[element.Tag, Element, int, int]] = [(tag, parent_element, 0, 0)]

        while len(nodeStack) > 0:
            if self.stop_loading: return

            tag, parent_element, inline_elements, depth = nodeStack.pop()

            children_to_sort: List[Tuple[element.Tag, Element, int, int]] = []

            for child_tag in tag.children:
                if isinstance(child_tag, element.Tag):
                    if child_tag.name in INLINE_ELEMENTS: inline_elements += 1
                    else: inline_elements = 0

                    child_tag.attrs["tag"] = child_tag.name
                    child_tag.attrs["text"] = child_tag.text.replace('\n', '')
                    child_tag.attrs["html"] = str(child_tag).replace('\n', '')

                    # head tags
                    if child_tag.name == "title": set_caption(BASE_TITLE + child_tag.attrs['text'])

                    text_rect: pg.Rect = parent_element.rect
                    text_rect_unused: pg.Rect = parent_element.rect_unused

                    # inherit parent styles
                    tag_styles: Dict[str, any] = parent_element.styles.copy()

                    # deepcopy if it contains nestled things like lists or whatever (points to the same reference)
                    if tag_styles is parent_element.styles: tag_styles: Dict[str, any] = deepcopy(parent_element.styles)

                    # add styles for text info when sizing fonts
                    tag_styles["text-tag-size"] = UI_TEXT_TAG_SIZES.get(child_tag.name, 16)
                    tag_styles["parent-tag-size"] = parent_element.styles.get("text-tag-size", 16)

                    if child_tag.name == 'i': tag_styles["italic"] = True
                    elif child_tag.name == 'b' or child_tag.name == 'strong': tag_styles["bold"] = True
                    elif child_tag.name == 'u': tag_styles["underline"] = True
                    elif child_tag.name == 'br':
                        if parent_element is not None and type(parent_element.rect) == pg.Rect:
                            new_line_height: int = feed_line(20, self.curr_y, tag_styles["font-size"], 16, 2)[1] - self.curr_y

                            parent_element.rect.height += new_line_height
                            self.curr_y += new_line_height
                        else:
                            self.curr_y += tag_styles["font-size"]

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
                            if child_tag.name in INLINE_ELEMENTS:
                                container_element = self.find_closest_container(parent_element)
                                if container_element is not None: container_element.rect.height += self.styled_text.renderStyledText('\n', )[0].height
                            
                            else:
                                new_line_height: int = feed_line(20, self.curr_y, tag_styles["font-size"], 16, 2)[1] - self.curr_y
                            
                                text_rect.height += new_line_height
                                self.curr_y += new_line_height
                        else:
                            tag_styles['font-size'] = UI_TEXT_TAG_SIZES.get(child_tag.name, 16)

                    # ---------- PARSING ----------

                    if "style" in child_tag.attrs:
                        self.css_parser.load_css_from_str_no_selector(tag_styles, child_tag.attrs["style"], child_tag.name, parent_element.styles["font-size"])

                    element_width: int = int(remove_units(str(child_tag.attrs.get("width", tag_styles.get("width", 0))),
                                                        parent_element.rect.width, parent_element.rect.width,
                                                        self.container_width, self.container_height))
                    
                    element_height: int = int(remove_units(str(child_tag.attrs.get("height", tag_styles.get("height", 0))),
                                                        parent_element.rect.height, parent_element.rect.height,
                                                        self.container_width, self.container_height))
                    
                    new_element: Element = Element(child_tag.name, child_tag.attrs, tag_styles, element_width,
                                                element_height, parent_element, inline_elements, depth)
                    
                    new_element.render(self.styled_text, 0, 0)

                    new_element.resize_family_rects(parent_element)

                    parent_element.children.append(new_element)

                    children_to_sort.append((child_tag, parent_element.children[-1], inline_elements, depth + 1))

            nodeStack.extend(reversed(children_to_sort))

    def reparse_element(self, browser_element: Element, style_overides: Dict[str, any] | None = None) -> None:
        """
        WARNING: THIS CODE IS AN ABSOLUTE MESS RIGHT NOW!!!
        """

        if style_overides == {}: style_overides = None

        element_as_bs4: element = BeautifulSoup(browser_element.attributes["html"], 'html.parser')
        element_as_bs4.attrs = browser_element.attributes

        elem_rect: pg.Rect = browser_element.rect

        self.styled_text.rendered_text.fill((255, 255, 255), elem_rect)

        # get the area underneath the element being changed
        surface_under_rect: pg.Rect = pg.Rect(0, elem_rect.y + elem_rect.height,
                                       self.styled_text.rendered_text.get_width(), self.styled_text.total_y - elem_rect.y)
        
        # save the area so it can be added back later
        surface_under: pg.Surface = pg.Surface((surface_under_rect.width, surface_under_rect.height))
        surface_under.blit(self.styled_text.rendered_text, (0, 0), surface_under_rect)

        # remove the area
        self.styled_text.rendered_text.fill((255, 255, 255), surface_under_rect)

        # move the 'cursor' back to the element in styled_text (moves it to the start of the area)
        self.styled_text.total_x = elem_rect.x
        self.styled_text.total_y = elem_rect.y

        element_status: Dict[str, any] = {
            "hovered": browser_element.hovered,
            "pressed": browser_element.pressed
        }

        browser_element.parent.children.remove(browser_element)

        #self.recurse_tag_children(element_as_bs4, browser_element.parent, browser_element.inline_index, browser_element.depth,
        #                          style_overides, element_status)

        self.populateElementTree(element_as_bs4, browser_element.parent)

        if surface_under_rect.height > self.styled_text.rendered_text.get_height():
            resized_rendered_text: pg.Surface = pg.Surface((self.styled_text.rendered_text.get_width(),
                                                            self.styled_text.rendered_text.get_height()\
                                                            +self.styled_text.render_height))
            resized_rendered_text.fill((255, 255, 255))
            resized_rendered_text.blit(self.styled_text.rendered_text, (0, 0))
            self.styled_text.rendered_text = resized_rendered_text

        # re-add the area
        self.styled_text.rendered_text.blit(surface_under, (surface_under_rect.x, self.styled_text.total_y + elem_rect.height))

        self.styled_text.total_y += surface_under_rect.height
        
    def parseHTML(self, html: str, thread_id: int = 0) -> Document | None:
        html = "<plazma-browser>\n" + html + "\n</plazma-browser>"

        soup = BeautifulSoup(html, 'html.parser')

        first_elem = soup.find()

        self.document.html_element = Element(first_elem.name, first_elem.attrs, {}, self.container_width, self.container_height)

        self.document.html_element.styles["view-width"] = self.container_width
        self.document.html_element.styles["view-height"] = self.container_height

        self.document.html_element.styles['font-size'] = 16

        #self.recurse_tag_children(first_elem, self.document.html_element)
        self.populateElementTree(first_elem, self.document.html_element)
        if self.stop_loading: return None

        logging.debug("Finished parsing html!")

        return self.document