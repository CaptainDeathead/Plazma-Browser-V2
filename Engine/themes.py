import pygame as pg
from config import GLOBAL_THEME_PATH
from typing import Dict
from json import dumps

class ThemeManager:
    COLOUR_STYLES: Dict[str, str] = {
        "color": "normal_text"
    }

    FONT_STYLES: Dict[str, str] = {
        "font-size": "size",
        "font": "font",
        "bold": "bold",
        "italic": "italic"
    }

    def __init__(self) -> None:
        """
        self.themes will be in format:

            {
                "@myclass": {
                    "key": "value"
                },

                "#myid": {
                    "key": "value"
                }
            }

        """

        self.themes: Dict[str, Dict[str, any]] = {}

    def generateTheme(self, machine_id: int, styles: Dict[str, any]) -> str:
        new_theme_id: str = f"#PLAZMA_BROWSER_MACHINE_GENERATED_ID_{machine_id}"

        self.themes[new_theme_id] = {"colours": {}, "font": {}}

        for style in styles:
            if style in self.COLOUR_STYLES:
                self.themes[new_theme_id]["colours"][self.COLOUR_STYLES[style]] = styles[style]
            elif style in self.FONT_STYLES:
                self.themes[new_theme_id]["font"][self.FONT_STYLES[style]] = styles[style]
            else:
                self.themes[new_theme_id][style] = styles[style]

        self.reloadFile()

        return new_theme_id
    
    def mergeStyles(self, styles1: Dict[str, any], theme_name: str) -> Dict[str, any]:
        if theme_name not in self.themes: raise KeyError(f"theme_name: `{theme_name}` not in self.themes!")

        styles1.update(self.themes[theme_name])

        return styles1

    def reloadFile(self) -> None:
        open(GLOBAL_THEME_PATH, 'w').write(dumps(self.themes))