import platform
from typing import Tuple

WIN_WIDTH: int = 800
WIN_HEIGHT: int = 600

HTML_LOAD_THREAD: bool = True


DEBUG_MODE: bool = True

GLOBAL_THEME_PATH: str = './Data/themes.json'



# --------------- BROWSER CONFIG ---------------

# platform settings
OS_NAME: str = platform.system()
OS_VERSION: str = platform.version()

OS_IDENT: str = f"({OS_NAME}; {OS_VERSION})"

# browser config
BROWSER_NAME: str = "Plazma"
BROWSER_VERSION: str = "0.1"

ENGINE_NAME: str = "WebIoniser"
ENGINE_VERSION: str = "0.1"

ADDITIONAL_INFO: str = "DevBuild (unstable)"

# general settings
LINK_NORMAL_COLOR: Tuple[int, int, int] = (65, 145, 245)
PRESSED_LINK_COLOR: Tuple[int, int, int] = (35, 170, 35)

# testing
BROWSER_TEST_URL: str = "https://en.wikipedia.org/wiki/web_browser"
#BROWSER_TEST_URL: str = "https://en.wikipedia.org/wiki/elon_musk"
#BROWSER_TEST_URL: str = "file://test.html"