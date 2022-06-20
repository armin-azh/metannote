from __future__ import annotations
from abc import ABC, abstractmethod

from .datatypes import *


class Dataset(ABC):

    def __init__(self):
        self._state = None

    @abstractmethod
    def build(self) -> None:
        pass

    def move_state(self, state: STATE) -> None:
        self._state = state
        self._state.dataset = self
