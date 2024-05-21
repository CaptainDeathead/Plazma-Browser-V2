import pygame as pg
import logging
from Engine.DOM.document import Document
from Engine.DOM.element import Element
from typing import Dict
from bs4 import BeautifulSoup, element
from pygame_gui import UIManager
from Ui.elements import UI_TEXT_TAG_SIZES, TEXT_TAGS, USE_TEXTBOX_TAGS
from Engine.STR.renderer import StyledText
from pygame.display import set_caption
from css_parser import parseString
from css_parser.css import CSSStyleSheet, CSSRuleList, CSSRule
from re import finditer

class HTMLParser:
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

                if child_tag.name == "title": set_caption(f"Plazma Browser (Dev) | {child_tag.attrs['text']}")

                text_rect: pg.Rect = None
                text_rect_unused: pg.Rect = None
                tag_styles: Dict[str, any] = {'font-size': str(UI_TEXT_TAG_SIZES.get(child_tag.name, 16)) + "px"}

                element_width: int = int(child_tag.attrs.get("width", 0))
                element_height: int = int(child_tag.attrs.get("height", 0))

                # ---------- NEW ----------

                child_tag_html: str = child_tag.attrs["html"]

                if child_tag.name in TEXT_TAGS:
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
                        
                    print(child_tag.attrs["html"] + '\n')
                
                # ---------- OLD ----------
                
                if child_tag.name in TEXT_TAGS:
                    # check if tag's text is empty
                    if child_tag.attrs["text"].replace(' ', '') == "": continue

                    if "style" in child_tag.attrs:
                        styles = child_tag.attrs["style"]

                        sheet: CSSStyleSheet = parseString(child_tag.name + "{ " + styles + " }")
                        
                        for rule in sheet:
                            for property in rule.style:
                                if property.name == 'font-family':
                                    tag_styles['font'] = property.value.split(',')[0]
                                else:
                                    tag_styles[property.name] = property.value

                    text_rect, text_rect_unused = self.styled_text.renderText(f"{child_tag.attrs['html']}\n\n", tag_styles)
                    
                parent_element.children.append(Element(child_tag.name, child_tag.attrs, text_rect, text_rect_unused,
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