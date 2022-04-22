from abc import ABC, abstractmethod
from typing import Iterable, Awaitable, Tuple
from itertools import chain

from game_receivers.game import Game


class GameReceiverHandler(ABC):
    """A base class for the `Chain of Responsibility` of the game receivers"""

    next: 'GameReceiverHandler' = None

    @abstractmethod
    def __await__(self):
        ...

    @abstractmethod
    def receive(self) -> Iterable[Awaitable[Game]]:
        """
        Receive all the games for this handler.
        """
        ...

    @classmethod
    @abstractmethod
    def picture(cls) -> Tuple[bytes, str]:
        """
        Get the pic to present to the gui
        """
        ...

    def set_next(self, next: 'GameReceiverHandler') -> 'GameReceiverHandler':
        self.next = next
        return self.next

    def get_games(self) -> Iterable[Awaitable[Game]]:
        return chain(self.receive(), self.next.get_games() if self.next is not None else [])