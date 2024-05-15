import logging
import requests
from io import TextIOWrapper
from Engine.DOM.document import Document
from Engine.renderer import Renderer
from config import HTML_LOAD_THREAD
from Engine.threads import LoaderThread

loader_thread: LoaderThread = None

def load_html(renderer: Renderer, html: str, mutable_document_class: Document | None) -> Document:
    if HTML_LOAD_THREAD:
        if mutable_document_class is None:
            raise Exception("Attempting to use separate thread for html loading but no mutable document class was found!")
        
        return load_nonblocking(renderer, html, mutable_document_class)
    
    else:
        return load_blocking(renderer, html)    

def load_blocking(renderer: Renderer, html: str) -> Document:
    document: Document = renderer.loadHTML(html)

    return document

def load_nonblocking(renderer: Renderer, html: str, mutable_document_class: Document) -> Document:
    global loader_thread

    if loader_thread is not None:
        renderer.html_parser.stop_loading = True
        loader_thread.join()

        renderer.html_parser.stop_loading = False
        loader_thread = None

    loader_thread = LoaderThread(target=renderer.loadHTML_NonBlocking, args=(html, mutable_document_class,), daemon=True)
    loader_thread.start()

    return mutable_document_class

def transfer_response(renderer: Renderer, response: requests.Response | TextIOWrapper | str) -> Document:
    document: Document = Document()
    
    if type(response) == str:
        logging.warning("Recieved error! Parsing error page...")
        document = load_html(renderer, open(f"./Pages/Error/{response}", "r").read(), document)
        
    elif type(response) == TextIOWrapper:
        logging.debug("Recieved response. Parsing contents...")
        document = load_html(renderer, response.read(), document)
        
    else:
        logging.debug("Recieved response. Parsing contents...")
        document = load_html(renderer, response.content.decode(encoding='utf-8', errors='surrogateescape'), document)

    return document

def get_page(url: str) -> requests.Response | str:
    if "file://" in url and url.index("file://") == 0:
        logging.debug(f"Attempting to open file: '{url}'.")
        
        try:
            return open(url.removeprefix("file://"), "r")
        
        except FileNotFoundError:
            logging.error("Cannot find file!")
            return "file_not_found.html"
        
        except Exception as e:
            logging.error(f"Cannot open file due to an unknown exception: '{e}'!")
            return "unknown_error.html"
    
    logging.debug(f"Attempting to connect to url: '{url}'.")

    try:
        response: requests.Response = requests.get(url, timeout=10, allow_redirects=True)
        logging.debug("Connection succeeded! Progressing to html parsing...")
        return response

    except (requests.ConnectionError, requests.ConnectTimeout, requests.Timeout):
        logging.error(f"Connection to: '{url}' failed due to a connection error!")
        return "connection_error.html"
    
    except requests.exceptions.HTTPError:
        logging.error(f"Connection to: '{url}' failed due to an invalid HTTP response!")
        return "http_error.html"
    
    except requests.TooManyRedirects:
        logging.error(f"Connection to: '{url}' failed because it attempted too many redirects!")
        return "redirect_error.html"
    
    except requests.exceptions.MissingSchema:
        logging.error(f"Connection to: '{url}' failed because it is an invalid url!")
        return "invalid_url_error.html"
    
    except Exception as e:
        logging.error(f"Connection to: '{url}' failed due to an unknown exception: '{e}'!")
        return "unknown_error.html"