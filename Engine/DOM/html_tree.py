from Engine.DOM.element import Element

from typing import Generator

class HTMLTree:
    def __init__(self) -> None:
        self.html_element: Element = Element(attributes={"tag": "html"})

    def get_elements(self) -> Generator[Element]:
        stack = [self.html_element]

        while len(stack) > 0:
            element = stack.pop(0)

            stack.extend(element.children)

            yield element