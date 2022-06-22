from __future__ import annotations
from collections.abc import Iterator, Iterable
from typing import List, Union
from pathlib import Path
from numpy import ndarray
from PIL import Image
from PIL.PngImagePlugin import PngImageFile
from PIL.JpegImagePlugin import JpegImageFile


class Dataformat:
    def __init__(self, **kwargs):
        self._image_path: Path = kwargs.get('image_path')
        self._bbox: ndarray = kwargs.get('bbox')
        self._categories: ndarray = kwargs.get('categories')
        self._width: int = kwargs.get('width')
        self._height: int = kwargs.get('height')

    @property
    def image_path(self) -> Path:
        return self._image_path

    @property
    def bbox(self) -> ndarray:
        return self._bbox

    @property
    def categories(self) -> ndarray:
        return self._categories

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def open_image(self) -> Union[PngImageFile, JpegImageFile, Image]:
        return Image.open(self._image_path)


class DataformatList(list):
    def __init__(self, **kwargs):
        self._categories = kwargs.get('categories')
        super(DataformatList, self).__init__()

    def __getitem__(self, item):
        return super(DataformatList, self).__getitem__(item - 1)


class DataIterator(Iterator):
    _position: int = None
    _reverse: bool = False

    def __init__(self, collection: DataformatList, reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value


class DataCollection(Iterable):
    def __init__(self, collection: Union[DataformatList, None] = None) -> None:
        if collection is None:
            collection = []
        self._collection = collection

    def __iter__(self) -> DataIterator:
        return DataIterator(self._collection)

    def get_reverse_iterator(self) -> DataIterator:
        return DataIterator(self._collection, reverse=True)

    def add_item(self, item: Dataformat):
        self._collection.append(item)
