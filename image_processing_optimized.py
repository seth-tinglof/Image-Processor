#!/usr/bin/env python3
# image_processing.py
from PIL import Image
from PIL import ImageFilter
from matplotlib.colors import rgb_to_hsv as mat_rgb_to_hsv
from matplotlib.colors import hsv_to_rgb as mat_hsv_to_rgb
from math import e
import numpy

__author__ = 'Seth Tinglof'
__version__ = '1.0'


class ImageProcessor:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, image):
        self.image = image
        self.IMAGE_BACKUP = image.copy()

    def convert_to_grayscale(self):
        """
        Converts the ImageProcessor's image object to grayscale.
        :return: None
        """
        self.image = self.image.convert("L").convert("RGB")

    def convert_to_black_and_white(self):
        """
        Converts ImageProcessor's image object to a black and white image.
        Accepts colored or grayscale images, but is inefficient for grayscale images.
        :return: None
        """
        self.image = self.image.convert("1").convert("RGB")

    def modify_saturation(self, amount):
        """
        Modifies saturation of the ImageProcessor's image object.
        :param amount: Scalar that saturation values will be modified by. Should be from 0 to 2
        :return: None
        """
        hsv = rgb_to_hsv(numpy.array(self.image))
        amount = e ** (1 - amount)
        hsv[..., 1] **= amount
        rgb = hsv_to_rgb(hsv)
        self.image = Image.fromarray(rgb, "RGB")

    def color_filter(self, color):
        """
        Makes the ImageProcessor's image object appear the color that is passed as an argument.
        :param color: color image is set to appear passed as a string. Supported colors are red, orange, green, blue,
        yellow, cyan, magenta, and violet.
        :return: None
        """
        color = color.lower()
        hue = 0
        if color == 'orange':
            hue = 1 / 12
        if color == 'green':
            hue = 1 / 3
        elif color == 'blue':
            hue = 2 / 3
        elif color == 'yellow':
            hue = 1 / 6
        elif color == 'cyan':
            hue = 1 / 2
        elif color == 'magenta':
            hue = 5 / 6
        elif color == 'violet':
            hue = 3 / 4

        array = numpy.array(self.image)
        self.image = Image.fromarray(set_hue(array, hue), "RGB")

    def invert_colors(self):
        self.image = Image.eval(self.image, lambda x: 255 - x)

    def average_pixel_color(self):
        """
        Changes every pixel in the ImageProcessor's image object to the average color of the initial image.
        :return: None
        """
        r, g, b = self.image.split()
        r = list(r.getdata())
        g = list(g.getdata())
        b = list(b.getdata())

        r_sum, g_sum, b_sum = 0, 0, 0
        for i in range(len(r)):
            r_sum += r[i]
            g_sum += g[i]
            b_sum += b[i]

        r = r_sum // len(r)
        g = g_sum // len(g)
        b = b_sum // len(b)

        self.image = Image.new("RGB", self.image.size, (r, g, b))

    def sepia_tone(self):
        """
        Gives the ImageProcessor's image the appearance of a sepia tone.
        :return: None
        """

        sepia_matrix = (
            0.393, 0.769, 0.189, 0,
            0.349, 0.686, 0.168, 0,
            0.272, 0.534, 0.131, 0)
        self.image = self.image.convert("RGB", sepia_matrix)

    def resize(self, scale):
        """
        Resize image to be its original width and height multiplied by a scaling factor.
        Note: this method produces a new image object rather than manipulating the old one,
        so pointers to the image set before this method is called will not point to the
        resized image but rather the original.
        :param scale: The value that the height and width are multiplied by.
        :return: None
        """
        self.image = self.image.resize((int(self.image.size[0] * scale), int(self.image.size[1] * scale)),
                                       Image.ANTIALIAS)

    def edge_detection(self):
        self.image = self.image.filter(ImageFilter.FIND_EDGES)

    def reset_image(self):
        """
        Sets the ImageProcessing image back to the default, i.e., the image which the ImageProcessing object was
        instantiated with
        :return: None
        """
        self.image = self.IMAGE_BACKUP.copy()

    def fit_to_screen(self, screen_width=1280, screen_height=720):
        """
        Re-sizes the image to fit on the screen.  Also changes the backup of the original image to this resized image.
        :param screen_width: Maximum width that the image can take up.
        :param screen_height: Maximum height that the image can take up.
        :return: None
        """
        if self.image.size[0] > screen_width or self.image.size[1] > screen_height:
            if self.image.size[0] / screen_width > self.image.size[1] / screen_height:
                self.resize(screen_width / self.image.size[0])
            else:
                self.resize(screen_height / self.image.size[1])
            self.IMAGE_BACKUP = self.image.copy()


def rgb_to_hsv(rgb):
    """
    Converts an RGB numpy array to an HSV numpy array.
    :param rgb: RBG numpy array.
    :return: HSV numpy array.
    """
    rgb = rgb.astype('float')
    rgb[..., 3:] = rgb[..., 3:] / 255
    return mat_rgb_to_hsv(rgb);


def hsv_to_rgb(hsv):
    """
    Converts an HSV numpy array image to an RGB numpy array image.
    :param hsv: HSV numpy array image.
    :return: RGB numpy array image.
    """
    rgb = mat_hsv_to_rgb(hsv)
    rgb[..., 3:] *= 255
    return rgb.astype('uint8')


def set_hue(array, hue):
    """
    Takes an input RGB numpy array image and returns the same image with the hue for each pixel set to the input hue.
    :param array: RGB numpy array image.
    :param hue: Hue that the image will be set to.
    :return: Numpy array image in RGB with new hue.
    """
    hsv = rgb_to_hsv(array)
    hsv[..., 0] = hue
    rgb = hsv_to_rgb(hsv)
    return rgb
