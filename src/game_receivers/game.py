from pydantic import BaseModel, Field
from typing import Tuple


class Game(BaseModel):
    name: str

    playtime: int = Field(default=-1)
    img: bytes = Field(default=None, repr=False)
    img_type: str = Field(default=None, repr=False)
    resent_playtime: Tuple[int, int] = Field(default=(-1, -1))
