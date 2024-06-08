from typing import List

class StyleNotIncludedException(Exception):
    def __init__(self, style_name: str, required_styles: List[str], ui_element_type: object) -> None:
        super().__init__(f"Style `{style_name}` not found! Required styles for `{ui_element_type.__name__}` are: {required_styles.__str__()}")