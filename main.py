from PyQt5.QtWidgets import QApplication, QWidget

from Engine.renderer import Renderer


class PlazmaBrowser:
    def __init__(self) -> None:
        self.app: QApplication = QApplication([])
        self.window: QWidget = QWidget()

        self.renderer: Renderer = Renderer()

        self.renderer.load_page("https://www.example.com")