# this provide a playground for easier import while debugging the code.


from ImageUtilities.image_io import open_image, write_image, as_matrix, as_image
from ImageUtilities.color_operations import to_grayscale
import os
import pdb


test_file = os.path.join(os.getcwd(), "resource", "sample", "test_image1.jpg")
output = os.path.join(os.getcwd(), "test", "test_grayscale.jpg")

if __name__ == '__main__':
    image = open_image(test_file)
    s = as_matrix(image)
    grey = to_grayscale(s)
    new_image = as_image(grey)
    print(grey.shape)
    write_image(new_image, output)


    pdb.set_trace()