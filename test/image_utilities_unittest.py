import ImageUtilities.image_io
import ImageUtilities.resize
import unittest
import os


class ImageUtilitiesUT(unittest.TestCase):

    """docstring for ImageUtilitiesUT"""

    def setUp(self):
        self.image_path = os.path.join(
            os.getcwd(), "resource", "sample", "test_image1.jpg")

    def test_load_image(self):
        image = ImageUtilities.image_io.open_image(self.image_path)
        image.close()

    def test_resize_image(self):
        image = ImageUtilities.image_io.open_image(self.image_path)

        # test only max_width
        output_path = os.path.join(os.getcwd(), "test", "test_resize1.jpg")
        new_image = ImageUtilities.resize.resize_image(image, max_width=1000)
        ImageUtilities.image_io.write_image(new_image, output_path)

        # test only max_height
        output_path = os.path.join(os.getcwd(), "test", "test_resize2.jpg")
        new_image = ImageUtilities.resize.resize_image(image, max_height=1000)
        ImageUtilities.image_io.write_image(new_image, output_path)

        # test_all
        output_path = os.path.join(os.getcwd(), "test", "test_resize3.jpg")
        new_image = ImageUtilities.resize.resize_image(
            image, max_width=1000, max_height=1000)
        ImageUtilities.image_io.write_image(new_image, output_path)

        # test_bigger
        output_path = os.path.join(os.getcwd(), "test", "test_resize4.jpg")
        new_image = ImageUtilities.resize.resize_image(image, max_width=5000)
        ImageUtilities.image_io.write_image(new_image, output_path)

        # close the buffer
        image.close()

    # def tearDown(self):
    #     for i in [1,2,3,4 ]:
    #         os.remove(
    #             os.path.join(os.getcwd(), "test", "test_resize{n}.jpg".format(n = str(i)))
    #             )


if __name__ == '__main__':
    unittest.main()
