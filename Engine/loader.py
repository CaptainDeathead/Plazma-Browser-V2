import logging
import requests
from io import TextIOWrapper
from Engine.DOM.document import Document
from Engine.renderer import Renderer

def transfer_response(renderer: Renderer, response: requests.Response | TextIOWrapper | str) -> Document:
    document: Document = Document()
    
    if type(response) == str:
        logging.warning("Recieved error! Parsing error page...")
        document = renderer.loadHTML(open(f"./Pages/Error/{response}", "r").read())
        
    elif type(response) == TextIOWrapper:
        logging.debug("Recieved response. Parsing contents...")
        document = renderer.loadHTML(response.read())
        
    else:
        logging.debug("Recieved response. Parsing contents...")
        document = renderer.loadHTML(response.content.decode(encoding='utf-8', errors='surrogateescape'))

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