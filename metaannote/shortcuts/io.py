from __future__ import annotations
from pathlib import Path
import json

from metaannote.datatypes import *


def read_coco(im_path: Path, ann_path: Path) -> COCO:
    """
    this function reads coco format dataset
    :TODO: this function will remove because it`s a part of Dataset classes
    :param im_path:
    :param ann_path:
    :return:
    """

    with open(str(ann_path), 'r') as f:
        parsed = json.load(f)

    images = {value['id']: value for value in parsed.get('images')}

    categories = {list(item.values())[0]: list(item.values())[1] for item in parsed.get('categories')}

    im_annotations: ANNOTATIONS = dict()
    for item in parsed.get('annotations'):
        im_id = item.get('image_id')
        item.pop('image_id')

        try:
            im_annotations[im_id].append(item)
        except KeyError:
            im_annotations[im_id] = [item]

    ds = []
    for im_id, item in images.items():
        p_image = im_path.joinpath(item.get('file_name'))
        bboxes = [val['bbox'] for val in im_annotations[im_id]]
        cat = [categories[val['category_id']] for val in im_annotations[im_id]]
        ds.append({
            'image_path': p_image,
            'bbox': bboxes,
            'categories': cat,
            'width': item.get('width'),
            'height': item.get('height')
        })

    return ds, categories


# if __name__ == '__main__':
#     ann_p = Path('/media/lizard/New Volume/Data/Drone/CustomeCocoDataset/Mobius/Train/Annotations/result.json')
#     im_p = Path('/media/lizard/New Volume/Data/Drone/CustomeCocoDataset/Mobius/Train/Annotations/images')
#
#     ds, cat = read_coco(im_path=im_p, ann_path=ann_p)
#
#     print(ds)
