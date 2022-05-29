from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractDatasetFactory(ABC):
    """
    this is abstract dataset factory
    """

    @abstractmethod
    def create_empty(self):
        """
        create an empty dataset which may be filled
        :return:
        """
        pass

    @abstractmethod
    def create(self):
        """
        create an empty dataset with some information
        :return:
        """
        pass
