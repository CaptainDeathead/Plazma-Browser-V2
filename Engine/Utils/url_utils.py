import logging
from typing import Tuple

browser_url: str = ""

def set_browser_url(new_url: str) -> None:
    global browser_url

    browser_url = new_url

def remove_whitespace(string: str) -> str:
    for i in range(len(string)):
        if string[i] != ' ': return string[i:]

def find_occurrences(string: str, char: str) -> Tuple[int]:
    return tuple(i for i, letter in enumerate(string) if letter == char)

def set_relative_path(url: str, relative_path: str) -> str:
    # url always contains '://' so we get the the third '/' if there is one else we just append to the end
    if url.count('/') > 2: return url[:find_occurrences(url, '/')[2]] + relative_path
    else: return url + relative_path

def resolve_url(base_url: str, url: str) -> str:
    global browser_url

    url = remove_whitespace(url)

    if url == "#": return base_url
    elif url.startswith("/"): return set_relative_path(base_url.replace("#", ""), url)
    elif url.startswith(("http", "https")): return url
    else:
        logging.warning(f"Cannot resolve url: '{url}' and cannot attach it to the base url!")
        return "#"
    
def resolve_url_in_browser_ctx(url: str) -> str:
    return resolve_url(browser_url, url)