class Interval:
    """An interval has left and right endpoints."""
    __slots__: tuple = "left", "right"

    def __init__(self, left: int, right: int) -> None:
        self.left: int = left
        self.right: int = right
    
    @property
    def width(self) -> int:
        return self.right - self.left

    def is_in(self, other) -> bool:
        return self.left >= other.left and self.right <= other.right
    
    def overlaps(self, other) -> bool:
        return min(self.right, other.right) - max(self.left, other.left) > 0

    def __str__(self) -> str:
        return f"[{self.left}, {self.right}]"


def timestamp_to_interval(task_start: str, task_end: str, day_start: str) -> Interval:
    """Convert timestamp of the endpoints to an Interval"""
    dstart: int = sum(int(elem) * 60**(1 - i) for i, elem in enumerate(day_start.split(':')))
    start: int = sum(int(elem) * 60**(1 - i) for i, elem in enumerate(task_start.split(':')))
    end: int = sum(int(elem) * 60**(1 - i) for i, elem in enumerate(task_end.split(':')))
    return Interval(start - dstart, end - dstart)
