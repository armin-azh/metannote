from pathlib import Path
from PIL import Image, ImageDraw
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbn

from metaannote.datatypes import *


def generate_color(cat: dict) -> dict:
    colors = {}
    for value in cat.values():
        colors[value] = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            1
        )

    return colors


def bbox_norm(xy: BOX, wh) -> BOX:
    w, h = wh

    width_height = xy[:, [2, 3]] - xy[:, [0, 1]]

    xy[:, 0] = ((xy[:, 0] + xy[:, 2]) / 2) / w
    xy[:, 1] = ((xy[:, 1] + xy[:, 3]) / 2) / h
    xy[:, 2] = width_height[:, 0] / w
    xy[:, 3] = width_height[:, 1] / h

    return xy


def visualize_annotation(o_path: Path, dataset: COCO, prefix='') -> None:
    o_path = o_path.joinpath(prefix)
    o_path.mkdir(parents=True, exist_ok=True)

    data, cat = dataset
    colors = generate_color(cat)

    for item in data:
        im_path: Path = item.get('image_path')

        im = Image.open(item.get('image_path'))
        im_draw = ImageDraw.Draw(im)
        categories = item.get('categories')
        bboxes = item.get('bbox')
        for idx in range(len(bboxes)):
            box = bboxes[idx]

            color = colors[categories[idx]]
            try:
                im_draw.rectangle(((box[0], box[1]), (box[0] + box[2], box[1] + box[3])), outline=color, width=2)
                im_draw.text((box[0], box[1]), categories[idx], color)
            except TypeError:
                im_draw.rectangle(((box[0], box[1]), (box[0] + box[2], box[1] + box[3])), outline='Red', width=2)
                im_draw.text((box[0], box[1]), categories[idx], 'Red')

        im.save(o_path.joinpath(im_path.name), )


def visualize_width_height_dist(o_path: Path, dataset: COCO, prefix='', labels=None) -> None:
    save_path = o_path.joinpath(prefix)
    save_path.mkdir(parents=True, exist_ok=True)

    data, cat = dataset
    re_cat = {value: key for key, value in cat.items()}
    ignore_labels = [re_cat[key] for key in labels] if isinstance(labels, list) else []

    total_boxes = np.empty((0, 2))
    categories = []

    for item in data:
        bbox = np.array(item.get('bbox'))
        categories += [re_cat[key] for key in item.get('categories')]
        total_boxes = np.concatenate([total_boxes, bbox[:, [2, 3]]], axis=0)

    categories = np.array(categories)

    fig = plt.figure(figsize=(8, 8))

    gs = fig.add_gridspec(2, 2, width_ratios=(7, 2), height_ratios=(2, 7),
                          left=0.1, right=0.9, bottom=0.1, top=0.9,
                          wspace=0.05, hspace=0.05)
    ax = fig.add_subplot(gs[1, 0])
    ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
    ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)
    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    x_hist = np.empty((0,))
    y_hist = np.empty((0,))

    for g in np.unique(categories):
        if g not in ignore_labels:
            idx = np.where(categories == g)[0]
            x_hist = np.concatenate([total_boxes[idx, 0], x_hist], axis=0)
            y_hist = np.concatenate([total_boxes[idx, 1], y_hist], axis=0)
            ax.scatter(x=total_boxes[idx, 0], y=total_boxes[idx, 1], label=cat[g])

    binwidth = 0.9
    xymax = max(np.max(np.abs(x_hist)), np.max(np.abs(y_hist)))
    lim = (int(xymax / binwidth) + 1) * binwidth

    bins = np.arange(0, lim + binwidth, binwidth)
    ax_histx.hist(x_hist, bins=bins)
    ax_histy.hist(y_hist, bins=bins, orientation='horizontal')
    ax.legend()
    ax.set_xlabel('Height'),
    ax.set_ylabel('Width')
    plt.show()


if __name__ == '__main__':
    from metaannote.shortcuts.io import read_coco

    # TODO: Test another dataset
    o_path = Path('/home/lizard/PycharmProjects/annotation_tool/output/')
    ann_p = Path('/home/lizard/PycharmProjects/annotation_tool/output/results.json')
    im_p = Path('/media/lizard/New Volume/Data/Drone/CustomeCocoDataset/Mobius/Train/Annotations/images')
    coco_dataset = read_coco(im_path=im_p, ann_path=ann_p)

    visualize_width_height_dist(o_path, coco_dataset, labels=["Airplane", "Helicopter"])
