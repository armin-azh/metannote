from __future__ import annotations
from collections.abc import Iterator, Iterable
from typing import Any, List


class DataIterator(Iterator):
    _position: int = None
    _reverse: bool = False

    def __init__(self, collection: List[Any], reverse: bool = False) -> None:
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
    def __init__(self, collection=None) -> None:
        if collection is None:
            collection = []
        self._collection = collection

    def __iter__(self) -> DataIterator:
        return DataIterator(self._collection)

    def get_reverse_iterator(self) -> DataIterator:
        return DataIterator(self._collection, reverse=True)

    def add_item(self, item: Any):
        self._collection.append(item)
