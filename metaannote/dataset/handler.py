from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional, List
from data_format import Dataformat

from .exceptions import HandlerBuildError


class Handler(ABC):

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler

        return handler

    @abstractmethod
    def handle(self, request: Any) -> Optional[str]:
        pass


class AugImFlip(AbstractHandler):
    def __init__(self, **kwargs):
        super(AugImFlip, self).__init__()
        self._vertical = kwargs.get('vertical') if kwargs.get('vertical') else False
        self._horizontal = kwargs.get('horizontal') if kwargs.get('horizontal') else False

        if not self._vertical and not self._horizontal: raise HandlerBuildError('AugImFlip: Both vertical and '
                                                                                'horizontal can`t be False')

    def handle(self, request: List[Dataformat]) -> List[Dataformat]:

        new_set = []

        for data in request:
            pass
