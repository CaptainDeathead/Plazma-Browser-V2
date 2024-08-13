from PyQt5.QtWidgets import QApplication, QWidget

class PlazmaBrowser:
    def __init__(self) -> None:
        self.app: QApplication = QApplication([])
        self.window: QWidget = QWidget()