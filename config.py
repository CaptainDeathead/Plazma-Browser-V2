import platform

WIN_WIDTH: int = 800
WIN_HEIGHT: int = 600

HTML_LOAD_THREAD: bool = True


DEBUG_MODE: bool = True

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

# testing
#BROWSER_TEST_URL: str = "https://en.wikipedia.org/wiki/web_browser"
BROWSER_TEST_URL: str = "file://test.html"