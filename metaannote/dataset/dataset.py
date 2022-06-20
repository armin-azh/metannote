from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union
from PIL import Image

from .data_format import DataCollection, DataIterator
from .datatypes import *


class Dataset(ABC):

    def __init__(self):
        self._state = None
        self._data_iterator: Union[None, DataIterator] = None
        self.build()

    def build(self, **kwargs) -> None:
        parsed_data = self.parse_data(**kwargs)

        rev = kwargs.get('reverse')
        if rev:
            self._data_iterator = DataCollection(collection=parsed_data).get_reverse_iterator()
        else:
            self._data_iterator = iter(DataCollection(collection=parsed_data))

    @abstractmethod
    def parse_data(self, **kwargs):
        pass

    def move_state(self, state: STATE) -> None:
        self._state = state
        self._state.dataset = self

    @staticmethod
    def open_image(im_path: IM_PATH) -> Image:
        return Image.open(im_path)

    def split(self):
        pass

    def generate(self):
        pass

    def augmentation(self):
        pass


class CocoDataset(Dataset):
    def __init__(self):
        super(CocoDataset, self).__init__()

    def parse_data(self, **kwargs):
        pass
