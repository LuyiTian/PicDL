import PIL.Image
import numpy as np
import sys
from basement.compatibility import basestring


def open_image(filepath):
    return PIL.Image.open(filepath)


def write_image(image, filepath):
    try:
        image.save(filepath)
    except Exception:
        return False

def as_matrix(filepath_or_image):
    if isinstance(filepath_or_image, basestring):
        return np.asarray(open_image(filepath_or_image))
    else:
        return np.asarray(filepath_or_image, dtype = np.uint8)


def as_image(matrix):
    if len(matrix.shape) == 2:
        grayscale = True
    result = PIL.Image.fromarray(matrix)
    if grayscale:
        return result.convert('RGB')
    else:
        return result
