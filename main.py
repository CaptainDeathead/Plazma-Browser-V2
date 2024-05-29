import pygame as pg
import pygame_gui as pgu
from Ui.search_bar import SearchBar
from Engine.renderer import Renderer
import requests
import logging
from Engine.DOM.document import Document
from Engine.loader import transfer_response, get_page
from threading import Thread
from config import *

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

pg.init()

class Window:
    def __init__(self):
        self.screen: pg.Surface = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.manager: pgu.UIManager = pgu.UIManager((WIN_WIDTH, WIN_HEIGHT))
        self.renderer: Renderer = Renderer(self.manager, 800, 550)
        self.document: Document = Document()
        
        self.search_bar: SearchBar = SearchBar(pg.Rect(200, 10, 400, 30), self.manager)
        
    def main(self):
        pg.display.set_caption("Plazma Browser (Dev) | New tab")

        if DEBUG_MODE:
            logging.debug("DEBUG_MODE=True; Loading test page...")
            self.search_bar.set_text(BROWSER_TEST_URL)
            response: requests.Response | str = get_page(BROWSER_TEST_URL)
            self.document = transfer_response(self.renderer, response)

        clock: pg.time.Clock = pg.time.Clock()
        while 1:
            time_delta = clock.tick(60)/1000.0
            self.screen.fill((255, 255, 255))
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                # scrolling
                elif event.type == pg.MOUSEWHEEL:
                    self.renderer.scroll_x -= event.x * 30
                    
                    if pg.key.get_pressed()[pg.K_LSHIFT]:
                        self.renderer.scroll_x -= event.y * 30
                    else:
                        self.renderer.scroll_y -= event.y * 30

                    # stop scrolling from going over the max-scroll limit
                    self.renderer.scroll_x = max(min(self.renderer.scroll_x, self.renderer.styled_text.rendered_text.get_width()-self.renderer.width), 0)
                    self.renderer.scroll_y = max(min(self.renderer.scroll_y, self.renderer.styled_text.rendered_text.get_height()-self.renderer.height), 0)
                    
                elif event.type == pgu.UI_TEXT_ENTRY_FINISHED:
                    response: requests.Response | str = get_page(self.search_bar.text)
                    self.document = transfer_response(self.renderer, response)
                    
                self.manager.process_events(event)

            self.screen.blit(self.renderer.render(), (0, 50))

            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)

            pg.display.flip()
            
if __name__ == "__main__":
    window: Window = Window()
    window.main()