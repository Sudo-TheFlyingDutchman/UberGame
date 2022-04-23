from pydantic import BaseModel, Field
from typing import Tuple


class Game(BaseModel):
    name: str

    playtime: int = Field(default=-1)
    img: bytes = Field(default=None, repr=False, exclude=True)
    img_type: str = Field(default=None, repr=False, exclude=True)
    resent_playtime: Tuple[int, int] = Field(default=(-1, -1))

    def __hash__(self):
        return self.name.__hash__() ^ self.playtime.__hash__() ^ self.resent_playtime.__hash__()