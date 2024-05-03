import pygame as pg
import pygame_gui as pgu
from Ui.search_bar import SearchBar
from Engine.renderer import Renderer
import requests
import logging
from Engine.DOM.document import Document
from io import TextIOWrapper

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

pg.init()

class Window:
    def __init__(self):
        self.screen: pg.Surface = pg.display.set_mode((800, 600))
        self.manager: pgu.UIManager = pgu.UIManager((800, 600))
        self.renderer: Renderer = Renderer(self.manager)
        self.document: Document = Document()
        
        self.search_bar: SearchBar = SearchBar(pg.Rect(200, 10, 400, 30), self.manager)

    def transfer_response(self, response: requests.Response | TextIOWrapper | str) -> None:
        if type(response) == str:
            logging.warning("Recieved error! Parsing error page...")
            self.document = self.renderer.loadHTML(open(f"./Pages/Error/{response}", "r").read())
            
        elif type(response) == TextIOWrapper:
            logging.debug("Recieved response. Parsing contents...")
            self.document = self.renderer.loadHTML(response.read())
            
        else:
            logging.debug("Recieved response. Parsing contents...")
            self.document = self.renderer.loadHTML(response.content.decode())

    def get_page(self, url: str) -> requests.Response | str:
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
        
    def main(self):
        clock: pg.time.Clock = pg.time.Clock()
        while 1:
            time_delta = clock.tick(60)/1000.0
            self.screen.fill((255, 255, 255))
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                    
                elif event.type == pgu.UI_TEXT_ENTRY_FINISHED:
                    response: requests.Response | str = self.get_page(self.search_bar.text)
                    self.transfer_response(response)
                    
                self.manager.process_events(event)

            self.screen.blit(self.renderer.html_parser.styled_text.rendered_text, (0, 50))
                
            self.manager.update(time_delta)
                    
            self.manager.draw_ui(self.screen)
            pg.display.flip()
            
if __name__ == "__main__":
    window: Window = Window()
    window.main()