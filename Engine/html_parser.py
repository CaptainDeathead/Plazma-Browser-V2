from Engine.DOM.document import Document
from Engine.DOM.element import Element
from typing import List
from bs4 import BeautifulSoup, element
from pygame_gui import UIManager
from Ui.elements import USE_TEXTBOX_TAGS, TEXT_TAGS
from Engine.STR.renderer import StyledText

class HTMLParser:
    def __init__(self, manager: UIManager, styled_text: StyledText):
        self.document: Document = Document()
        self.manager: UIManager = manager
        self.styled_text: StyledText = styled_text
        self.curr_y: int = 50

    def recurse_tag_children(self, tag: element.Tag, parent_element: Element):
        for child_tag in tag.children:
            if isinstance(child_tag, element.Tag):
                child_tag.attrs["tag"] = child_tag.name
                child_tag.attrs["text"] = child_tag.text
                child_tag.attrs["html"] = str(child_tag)

                if child_tag.name in TEXT_TAGS:
                    self.styled_text.html_text += f"{child_tag.attrs['html']}\n"
                    continue

                parent_element.children.append(Element(child_tag.name, child_tag.attrs))

                self.recurse_tag_children(child_tag, parent_element.children[-1])
        
    def parseHTML(self, html: str):
        soup = BeautifulSoup(html, 'html.parser')

        first_elem = soup.find()

        self.document.html_element = Element(first_elem.name, first_elem.attrs)

        self.recurse_tag_children(first_elem, self.document.html_element)
        self.styled_text.render()

        return self.document