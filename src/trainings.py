import google_api.calendar
from datetime import datetime


class TrainingType:
    def __init__(
        self, type: str = "Dinamica", priority: int = None, lock: bool = False
    ) -> None:
        self.type = type
        self.priority = priority
        self.lock = lock

    def __eq__(self, other: object) -> bool:
        return self.type == other.type

