import PIL.Image
import numpy as np
from .image_io import open_image, write_image 

def resize_image(image, max_width = None, max_height = None, preserve_transparency = False):
    '''
    Support transparent image
    '''
    assert not(max_width is None and max_height is None)
    rgba = np.asarray(image, dtype=np.uint8)
    rgba2 = np.asarray(image, dtype=np.uint8)
    rgba2.flags.writeable = True
    original_height, orignal_width = rgba.shape[0], rgba.shape[1]
    if preserve_transparency:
        for y in range(original_height):
            for x in range(orignal_width):
                if rgba[y,x,3] != 0:
                    continue
                col_sum = np.zeros((3), dtype=np.uint16)
                i = 0
                for oy in [-1,0,1]:
                    for ox in [-1,0,1]:
                        if not oy and not ox:
                            continue
                        iy = y + oy
                        if iy <0 or iy >= original_height:
                            continue
                        ix = x + ox
                        if ix <0 or ix >= orignal_width:
                            continue
                        col = rgba[iy, ix]
                        if not col[3]:
                            continue
                        colSum += col[:3]
                        i += 1
                rgba2[y,x, :3] = colSum / i

    new_image = PIL.Image.fromarray(rgba2)
    if max_height is None:
        max_height = int(float(max_width) / float(orignal_width) * original_height)
    if max_width is None:
        max_width = int(float(max_height) / float(original_height) * orignal_width)


    new_image = new_image.transform((max_width, max_height), PIL.Image.EXTENT, (0,0) + new_image.size, PIL.Image.LINEAR)
    return new_image
