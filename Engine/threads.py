from threading import Thread
from typing import Iterable

class LoaderThread(Thread):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)