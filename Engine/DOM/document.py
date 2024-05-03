from Engine.DOM.element import Element

class Document:
    def __init__(self):
        self.html_element: Element = None

    def createElement(self, tag: str):
        ...