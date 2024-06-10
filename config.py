import platform
from typing import Tuple

WIN_WIDTH: int = 800
WIN_HEIGHT: int = 600

BUTTON_SCROLL_INCREMENT: int = 100

HTML_LOAD_THREAD: bool = True


DEBUG_MODE: bool = True
SHOW_PRIMARY_SURFACE_CONTAINERS: bool = False

# platform settings
OS_NAME: str = platform.system()
OS_VERSION: str = platform.version()

OS_IDENT: str = f"({OS_NAME}; {OS_VERSION})"

# browser config
BROWSER_NAME: str = "Plazma Browser"
BROWSER_VERSION: str = "0.1.0dev"

ENGINE_NAME: str = "WebIoniser"
ENGINE_VERSION: str = "0.1.0dev"

ADDITIONAL_INFO: str = "DevBuild (unstable)"

BASE_TITLE: str = f"{BROWSER_NAME}_v{BROWSER_VERSION} | {ENGINE_NAME}_v{ENGINE_VERSION} | INFO: {ADDITIONAL_INFO} | "

# general settings
LINK_NORMAL_COLOR: Tuple[int, int, int] = (65, 145, 245)
PRESSED_LINK_COLOR: Tuple[int, int, int] = (35, 170, 35)

# testing
BROWSER_TEST_URL: str = "https://en.wikipedia.org/wiki/web_browser"
#BROWSER_TEST_URL: str = "https://en.wikipedia.org/wiki/elon_musk"
#BROWSER_TEST_URL: str = "https://google.com"
#BROWSER_TEST_URL: str = "file://test.html"