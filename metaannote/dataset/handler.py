from __future__ import annotations
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Optional, List
from PIL import ImageOps, ImageFilter, ImageEnhance
from data_format import Dataformat

from .exceptions import HandlerBuildError


class Handler(ABC):

    @abstractmethod
    def __call__(self, request, **kwargs) -> Optional[str]:
        pass


class AugImFlip(Handler):
    def __init__(self, **kwargs):
        super(AugImFlip, self).__init__()
        self._vertical = kwargs.get('vertical') if kwargs.get('vertical') else False
        self._horizontal = kwargs.get('horizontal') if kwargs.get('horizontal') else False

        if not self._vertical and not self._horizontal: raise HandlerBuildError('AugImFlip: Both vertical and '
                                                                                'horizontal can`t be False')

    def __call__(self, request: List[Dataformat], **kwargs) -> List[Dataformat]:
        save_path = Path(kwargs.get('save_path'))
        n_list = []

        for idx, data in enumerate(request):
            n_list.append(data)
            filename = data.image_path.stem
            name_hash = self.__class__.__name__
            d_save = save_path.joinpath(f"{filename}_{name_hash}_{idx + 1}.{data.image_path.suffix}")

            im = data.open_image

            if self._horizontal:
                im = ImageOps.mirror(im)
            if self._vertical:
                im = ImageOps.flip(im)

            im.save(d_save)

            n_df = {
                'image_path': d_save,
                'bbox': data.bbox,
                'categories': data.categories,
                'width': data.width,
                'height': data.height
            }

            n_list.append(Dataformat(**n_df))

        return n_list


class AugImCenterCrop(Handler):
    def __init__(self, **kwargs):
        super(AugImCenterCrop, self).__init__()
        self._percentage = kwargs.get('percentage') if kwargs.get('percentage') else 0.5

        if not (0 < self._percentage <= 1): HandlerBuildError(
            'AugImCenterCrop: percentage value must be between 0 and 1')

    def __call__(self, request: List[Dataformat], **kwargs) -> List[Dataformat]:
        pass
