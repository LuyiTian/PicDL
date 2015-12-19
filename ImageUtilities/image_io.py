import PIL.Image

def open_image(filepath):
    return PIL.Image.open(filepath)


def write_image(image, filepath):
    try:
        image.save(filepath)
    except Exception:
        raise e
