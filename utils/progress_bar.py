from dataclasses import dataclass
from typing import Final, Union, Optional

from tqdm import tqdm

from conf import alog

RED: Final[str] = "RED"
MAGENTA: Final[str] = "magenta"

BLUE: Final[str] = "BLUE"
WHITE: Final[str] = 'WHITE'
YELLOW: Final[str] = "YELLOW"  # '\x1b[33m' Typing doesn't support color strings
CYAN: Final[str] = "CYAN"
GREEN: Final[str] = "GREEN"

BLACK: Final[str] = "BLACK"


@dataclass
class ProgressBar:
    color: Union[BLACK, RED, MAGENTA, BLUE, WHITE, YELLOW, CYAN, GREEN] = MAGENTA
    kwargs: dict = None

    pb = None

    def __post_init__(self):
        kwargs = self.kwargs or {}

        self.pb = tqdm([], colour=self.color, **kwargs)

    def add(self, increment: float = 1):
        if increment < 0:
            raise ValueError(f"invalid increment {increment}")
        self.pb.total += increment
        self.pb.refresh()

    def update(self, noOfDoneTasks: Optional[float] = 1):
        if noOfDoneTasks < 0:
            raise ValueError(f"invalid no of done tasks {noOfDoneTasks}")
        self.pb.update(noOfDoneTasks)

    def refresh(self):
        alog.debug("refreshing the progress bar")
        self.pb.refresh()
