from typing import Dict, List
from Ui.elements import *

class Element:
    def __init__(self, tag: str, attributes: Dict):
        self.tag: str = tag
        self.attributes: Dict = attributes
        self.children: List = []