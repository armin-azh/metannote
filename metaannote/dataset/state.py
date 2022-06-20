from __future__ import annotations
from abc import ABC, abstractmethod

from .datatypes import *


class State(ABC):

    def __init__(self):
        self._dataset = None

    @property
    def dataset(self) -> DATASET:
        return self._dataset

    @dataset.setter
    def dataset(self, dataset: DATASET):
        self._dataset = dataset

    @abstractmethod
    def next_state(self) -> None:
        pass

    @abstractmethod
    def failure(self) -> None:
        pass


class SplitState(State):
    def __init__(self):
        super(SplitState, self).__init__()

    def next_state(self) -> None:
        self.dataset.move_state(PreProcessingState())

    def failure(self) -> None:
        self.dataset.move_state(SplitState())


class PreProcessingState(State):
    def __init__(self):
        super(PreProcessingState, self).__init__()

    def next_state(self) -> None:
        self.dataset.move_state(AugmentationState())

    def failure(self) -> None:
        self.dataset.move_state(SplitState())


class AugmentationState(State):
    def __init__(self):
        super(AugmentationState, self).__init__()

    def next_state(self) -> None:
        self.dataset.move_state(GeneratingState())

    def failure(self) -> None:
        self.dataset.move_state(SplitState())


class GeneratingState(State):
    def __init__(self):
        super(GeneratingState, self).__init__()

    def next_state(self) -> None:
        self.dataset.move_state(SplitState())

    def failure(self) -> None:
        self.dataset.move_state(SplitState())
