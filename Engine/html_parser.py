import pygame as pg
import logging
from Engine.DOM.document import Document
from Engine.DOM.element import Element
from typing import Dict
from bs4 import BeautifulSoup, element
from pygame_gui import UIManager
from Ui.elements import UI_TEXT_TAG_SIZES, TEXT_TAGS, USE_TEXTBOX_TAGS
from Engine.STR.renderer import StyledText, remove_units
from pygame.display import set_caption
from css_parser import parseString
from css_parser.css import CSSStyleSheet, CSSRuleList, CSSRule
from re import finditer
from copy import deepcopy

class HTMLParser:
    CONTAINER_WIDTH: int = 0
    CONTAINER_HEIGHT: int = 0

    def __init__(self, manager: UIManager, styled_text: StyledText) -> None:
        self.document: Document = Document()
        self.manager: UIManager = manager
        self.styled_text: StyledText = styled_text
        self.curr_y: int = 50
        self.stop_loading: bool = False

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

                if child_tag.name == 'i': tag_styles["italic"] = True
                elif child_tag.name == 'b' or child_tag.name == 'strong': tag_styles["bold"] = True
                elif child_tag.name == 'u': tag_styles["underline"] = True
                elif child_tag.name == 'br':
                    if parent_element is not None and type(parent_element.rect) == pg.Rect:
                        parent_element.rect.height += self.styled_text.renderStyledText('\n')[0].height
                    else:
                        self.styled_text.renderStyledText('\n')[0].height

                element_width: int = int(remove_units(str(child_tag.attrs.get("width", 0))))
                element_height: int = int(remove_units(str(child_tag.attrs.get("height", 0))))

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
                
                # ----- OLD -----

                """if child_tag.name in TEXT_TAGS:
                    # check if tag's text is empty
                    if child_tag.attrs["text"].replace(' ', '') == "": continue

                    text_rect, text_rect_unused = self.styled_text.renderText(f"{child_tag.attrs['html']}\n\n", tag_styles)
                    
                    parent_element.children.append(Element(child_tag.name, child_tag.attrs, text_rect, text_rect_unused,
                                                        tag_styles, element_width, element_height))
                else:
                    parent_element.children.append(Element(child_tag.name, child_tag.attrs, {0, 0, self.CONTAINER_WIDTH, self.CONTAINER_HEIGHT}, {0, 0, 0, 0},
                                                        tag_styles, element_width, element_height))"""
                    
                # ----- NEW -----

                if child_tag.name == 'browser_text':
                    text_rect, text_rect_unused = self.styled_text.renderStyledText(f"{child_tag.attrs['text']}", tag_styles)

                    parent_element.children.append(Element(child_tag.name, child_tag.attrs, text_rect, text_rect_unused,
                                                        tag_styles, element_width, element_height))
                else:
                    parent_element.children.append(Element(child_tag.name, child_tag.attrs, {0, 0, self.CONTAINER_WIDTH, self.CONTAINER_HEIGHT}, {0, 0, 0, 0},
                                                        tag_styles, element_width, element_height))

                self.recurse_tag_children(child_tag, parent_element.children[-1])
        
    def parseHTML(self, html: str, thread_id: int = 0) -> Document | None:
        soup = BeautifulSoup(html, 'html.parser')

        first_elem = soup.find()

        self.document.html_element = Element(first_elem.name, first_elem.attrs)

        self.recurse_tag_children(first_elem, self.document.html_element)
        if self.stop_loading: return None

        logging.debug("Finished parsing html!")

        return self.document