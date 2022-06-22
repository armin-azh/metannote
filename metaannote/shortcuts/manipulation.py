from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import PIL
from pathlib import Path


def flip_image(im, vertical: bool, horizontal: bool):
    if vertical:
        im = ImageOps.flip(im)
    if horizontal:
        im = ImageOps.mirror(im)

    return im


def rotate(im, angle, clockwise=True):
    if clockwise:
        return im.rotate(-angle, PIL.Image.NEAREST, expand=1)
    else:
        return im.rotate(angle, PIL.Image.NEAREST, expand=1)


def center_crop(im, percent):
    width, height = im.size

    new_width = width * percent
    new_height = height * percent

    left = (width - new_width) / 2
    top = (height - new_height) / 2

    right = (width + new_width) / 2
    bottom = (height + new_height) / 2

    return im.crop((left, top, right, bottom))


def brightness(im, percentage, dark=True):
    if not dark:
        percentage = 3 * percentage
    return ImageEnhance.Brightness(im).enhance(percentage)


def blur(im, pixel):
    return im.filter(ImageFilter.GaussianBlur(pixel))


if __name__ == '__main__':
    im_path = Path('/home/lizard/PycharmProjects/annotation_tool/output/0b2bf75b-vlcsnap-00035.png')
    im = Image.open(im_path)
    print(type(im))
    im.show()
