from interval import Interval


class Task:
    """A Task is the activities to be scheduled."""
    __slots__: tuple = "id", "name", "day", "interval"  # streamline memory usage

    def __init__(self, id: int, name: str, day: int, interval: Interval) -> None:
        self.id: int = id
        self.name: str = name
        self.day: int = day
        self.interval : Interval = interval
    
    def __str__(self) -> str:
        return f"{self.id}-{self.name}-Day {self.day} {self.interval}"