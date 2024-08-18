from Engine.exceptions import MissingAttributeError

from typing import List, Dict

class Element:
    def __init__(self, attributes: Dict[str, any]) -> None:
        self._unpack_attributes(attributes)

        self.children: List[Element] = []

    def _unpack_attributes(self, attributes: Dict[str, any]) -> None:
        self.tag: str = attributes.get("tag", MissingAttributeError(self._required_attrs, "tag"))
        self.element_id: str = attributes.get("id", "")
        self.element_class: str = attributes.get("class", "")