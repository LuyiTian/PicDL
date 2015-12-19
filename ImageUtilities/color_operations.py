import PIL.Image
import numpy as np
from .image_io import open_image, write_image
from scipy import misc


def to_grayscale(image, rgb_weights = None):
    if rgb_weights is None:
        rgb_weights = [1./3] * 3

    return np.dot(image[...,:3], rgb_weights)
