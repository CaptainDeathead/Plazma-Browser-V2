import logging
from cssutils import parseString
from cssutils.css import CSSStyleSheet
from cssutils import log as cssutils_log
from typing import Dict, Tuple
from Engine.Utils.utils import remove_units, ishex, hex_to_rgb, containsnum

cssutils_log.setLevel(logging.CRITICAL)

class CSSParser:
    """
    CSS parser / manager for Plazma Browser
    """

    def __init__(self, container_width: int, container_height: int) -> None:
        self.container_width: int = container_width
        self.container_height: int = container_height

    def add_style(self, style_with_value: Tuple[str, str], styles: Dict[str, any]):
        style, value = style_with_value

        if style == "font": styles["font"] = value
        elif style == "font-size": styles["font-size"] = int(remove_units(value, styles.get("text-tag-size", 16), styles.get("parent-tag-size", 16), styles["view-width"], styles["view-height"]))
        elif style == "background-color" or style == "color" and (type(value) == tuple or type(value) == str):
            if ishex(value): styles[style] = hex_to_rgb(value)
            else: styles[style] = value

        else: styles[style] = value

    def load_css_from_str_no_selector(self, styles: Dict[str, any], styles_string: str, selector: str, parent_size: int) -> Dict[str, any]:
        sheet: CSSStyleSheet = parseString(selector + "{ " + styles_string + " }")
        
        for rule in sheet:
            for property in rule.style:
                if property.name == 'font-family':
                    styles['font-name'] = property.value.split(',')[0]
                else:
                    value: str | float | int = property.value

                    if type(value) == str:
                        if ishex(value): value = hex_to_rgb(value)

                        elif containsnum(value):
                            value = remove_units(value, styles["font-size"], parent_size, self.container_width, self.container_height)
                        
                    styles[property.name] = value

        return styles