import pygame as pg
import pygame_gui as pgu
import requests
import logging
from multiprocessing import Process, Queue
from Ui.search_bar import SearchBar
from Ui.scrollbar import HScrollBar, VScrollBar
from Ui.button import PGUButton
from Engine.renderer import Renderer
from Engine.loader import transfer_response, get_page
from devtools import start_inspector
from config import *

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

devtools_update_queue: Queue = Queue()
devtools_patch_queue: Queue = Queue()

devtools_proc: Process | None = None

if DEVTOOLS_ENABLED:
    devtools_proc = Process(target=start_inspector, args=(devtools_update_queue, devtools_patch_queue))
    devtools_proc.start()

pg.init()

class Window:
    def __init__(self):
        self.screen: pg.Surface = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pg.RESIZABLE)
        self.manager: pgu.UIManager = pgu.UIManager((WIN_WIDTH, WIN_HEIGHT))
        self.renderer: Renderer = Renderer(self.manager, WIN_WIDTH, WIN_HEIGHT-50, self.load_page)
        
        self.search_bar: SearchBar = SearchBar(pg.Rect(200, 10, WIN_WIDTH-400, 30), self.manager)
        
        self.h_scroll_bar: HScrollBar = HScrollBar(self.manager, pg.Rect(0, WIN_HEIGHT-20, WIN_WIDTH-20, 20), WIN_WIDTH-20, self.renderer.move_scroll_x)
        self.v_scroll_bar: VScrollBar = VScrollBar(self.manager, pg.Rect(WIN_WIDTH-20, 50, 20, WIN_HEIGHT-70), WIN_HEIGHT-70, self.renderer.move_scroll_y)
        
    def load_page(self, url: str) -> None:
        response: requests.Response | str = get_page(url)
        transfer_response(self.renderer, response)

    def main(self):
        global WIN_WIDTH, WIN_HEIGHT

        pg.display.set_caption(BASE_TITLE + "New tab")

        if DEBUG_MODE:
            logging.debug("DEBUG_MODE=True; Loading test page...")
            self.search_bar.set_text(BROWSER_TEST_URL)
            response: requests.Response | str = get_page(BROWSER_TEST_URL)
            transfer_response(self.renderer, response)

        clock: pg.time.Clock = pg.time.Clock()
        while 1:
            time_delta = clock.tick(60)/1000.0
            self.screen.fill((255, 255, 255))
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.image.save(self.renderer.html_parser.styled_text.rendered_text, "final.png")

                    if devtools_proc is not None: devtools_proc.kill()

                    pg.quit()
                    exit()

                # scrolling
                elif event.type == pg.MOUSEWHEEL:
                    self.renderer.move_scroll_x(-event.x * 30)
                    
                    if pg.key.get_pressed()[pg.K_LSHIFT]:
                        self.renderer.move_scroll_x(-event.y * 30)
                    else:
                        self.renderer.move_scroll_y(-event.y * 30)

                elif event.type == pg.VIDEORESIZE:
                    WIN_WIDTH, WIN_HEIGHT = self.screen.get_width(), self.screen.get_height()

                    self.manager.set_window_resolution((WIN_WIDTH, WIN_HEIGHT))

                    self.search_bar.set_dimensions((WIN_WIDTH-400, 30))

                    self.h_scroll_bar.resize(pg.Rect(0, WIN_HEIGHT-20, WIN_WIDTH-20, 20))
                    self.v_scroll_bar.resize(pg.Rect(WIN_WIDTH-20, 50, 20, WIN_HEIGHT-70))

                    self.renderer.resize(WIN_WIDTH, WIN_HEIGHT)
                    
                elif event.type == pgu.UI_TEXT_ENTRY_FINISHED: self.load_page(self.search_bar.text)
                    
                elif event.type == pgu.UI_BUTTON_PRESSED:
                    if type(event.ui_element) == PGUButton:
                        event.ui_element.click_action()

                self.manager.process_events(event)

            if self.renderer.just_finished_loading:
                if devtools_proc is not None:
                    logging.debug("Renderer has finished loading. Sending top level element to DevTools...")
                    devtools_update_queue.put(self.renderer.html_parser.document.html_element)
                
                self.renderer.just_finished_loading = False

            self.screen.blit(self.renderer.render(), (0, 50))

            if self.renderer.scroll_x != self.h_scroll_bar.scroll \
              or self.renderer.styled_text.rendered_text.get_width() != self.h_scroll_bar.max_scroll:
                self.h_scroll_bar.set_scroll(self.renderer.scroll_x, self.renderer.styled_text.rendered_text.get_width())

            if self.renderer.scroll_y != self.v_scroll_bar.scroll \
              or self.renderer.styled_text.rendered_text.get_height() != self.v_scroll_bar.max_scroll:
                self.v_scroll_bar.set_scroll(self.renderer.scroll_y, self.renderer.styled_text.rendered_text.get_height())

            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)

            self.h_scroll_bar.draw(self.screen)
            self.v_scroll_bar.draw(self.screen)

            pg.display.flip()
            
if __name__ == "__main__":
    window: Window = Window()
    window.main()