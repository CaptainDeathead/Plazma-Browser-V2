

from typing import Dict

class MissingAttributeError(Exception):
    def __init__(self, required_attrs: Dict[str, any], offender: str) -> None:
        super().__init__(f"Required attribute '{offender}' not found!\nRequired attributes are '{required_attrs.__str__()}'.")