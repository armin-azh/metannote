from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union
from PIL import Image
from pathlib import Path
import json

from .data_format import DataCollection, DataIterator, Dataformat, DataformatList
from .datatypes import *
from .exceptions import *


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
    def parse_data(self, **kwargs) -> DataformatList:
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

    def parse_data(self, **kwargs) -> DataformatList:
        dir_im = kwargs.get('image_dir')
        if dir_im is None:
            raise DatasetParsedError(f"Coco dataset parsed: you need to enter image_dir")

        dir_im: Path = Path(dir_im)
        path_ann = kwargs.get('annotation')

        if path_ann is None:
            raise DatasetParsedError(f'Coco dataset parsed: you need to enter path_ann')

        path_ann: Path = Path(path_ann)

        with open(str(path_ann), 'r') as f:
            parsed_ann = json.load(f)

        images: dict = {value['id']: value for value in parsed_ann.get('images')}
        categories = {list(item.values())[0]: list(item.values())[1] for item in parsed_ann.get('categories')}

        im_annotations = dict()
        for item in parsed_ann.get('annotations'):
            im_id = item.get('image_id')
            item.pop('image_id')
            try:
                im_annotations[im_id].append(item)
            except KeyError:
                im_annotations[im_id] = [item]

        ds = DataformatList(categories=categories)
        for im_id, item in images.items():
            p_image = dir_im.joinpath(item.get('file_name'))
            bboxes = [val['bbox'] for val in im_annotations[im_id]]
            cat = [categories[val['category_id']] for val in im_annotations[im_id]]
            n_df = {
                'image_path': p_image,
                'bbox': bboxes,
                'categories': cat,
                'width': item.get('width'),
                'height': item.get('height')
            }
            ds.append(Dataformat(**n_df))
        return ds
