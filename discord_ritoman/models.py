import enum


class GameResult(enum.Enum):
    NONE = 0
    WIN = 1
    LOSS = 2


class GameMode(enum.Enum):
    UNDEFINED = 0
    RANKED = 1
    NORMAL = 2
    ARAM = 3
    RGM = 4
