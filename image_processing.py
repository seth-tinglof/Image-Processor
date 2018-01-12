#!/usr/bin/env python3
# image_processing.py
from PIL import Image
from PIL import ImageFilter
from colorsys import rgb_to_hsv
from colorsys import hsv_to_rgb

__author__ = 'Seth Tinglof'
__version__ = '1.0'


class ImageProcessor:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, image):
        self.image = image
        self.pixels = self.image.load()
        self.IMAGE_BACKUP = image.copy()

    def convert_to_grayscale(self):
        """
        Converts the ImageProcessor's image object to grayscale.
        :return: None
        """
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                r, g, b = self.pixels[i, j]
                avg = int((r * .2989 + g * .5870 + b * .1140))
                self.pixels[i, j] = (avg, avg, avg)

    def convert_to_black_and_white(self, threshold):
        """
        Converts ImageProcessor's image object to a black and white image.
        Accepts colored or grayscale images, but is inefficient for grayscale images.
        :param threshold: The amount of light (from 0 to 255) that a pixel must have to be white instead of black.
        :return: None
        """
        self.convert_to_grayscale()
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                if self.pixels[i, j][0] >= threshold:
                    self.pixels[i, j] = self.WHITE
                else:
                    self.pixels[i, j] = self.BLACK

    def modify_saturation(self, amount):
        """
        Modifies saturation of the ImageProcessor's image object.
        :param amount: Scalar that saturation values for each pixel are multiplied by.
        :return: None
        """
        if amount < 0:
            amount *= -1
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                r, g, b = self.pixels[i, j]
                h, s, v = rgb_to_hsv(r / 255, g / 255, b / 255)
                s *= amount
                if s > 1:
                    s = 1.0
                r, g, b = hsv_to_rgb(h, s, v)
                r = int(r * 255)
                g = int(g * 255)
                b = int(b * 255)
                self.pixels[i, j] = (r, g, b)

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

        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                r, g, b = self.pixels[i, j]
                h, s, v = rgb_to_hsv(r / 255, g / 255, b / 255)
                h = hue
                r, g, b = hsv_to_rgb(h, s, v)
                r = int(r * 255)
                g = int(g * 255)
                b = int(b * 255)
                self.pixels[i, j] = (r, g, b)

    def invert_colors(self):
        self.image = Image.eval(self.image, lambda x: 255 - x)
        self.pixels = self.image.load()

    def average_pixel_color(self):
        """
        Changes every pixel in the ImageProcessor's image object to the average color of the initial image.
        :return: None
        """
        r = 0
        g = 0
        b = 0
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                r += self.pixels[i, j][0]
                g += self.pixels[i, j][1]
                b += self.pixels[i, j][2]
        r //= self.image.size[0] * self.image.size[1]
        g //= self.image.size[0] * self.image.size[1]
        b //= self.image.size[0] * self.image.size[1]

        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                self.pixels[i, j] = (r, g, b)

    def sepia_tone(self):
        """
        Gives the ImageProcessor's image the appearance of a sepia tone.
        :return: None
        """
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                r, g, b = self.pixels[i, j]
                r2 = int(r * 0.393 + g * 0.769 + b * 0.189)
                g2 = int(r * 0.349 + g * 0.686 + b * 0.168)
                b2 = int(r * 0.272 + g * 0.534 + b * 0.131)
                self.pixels[i, j] = (r2, g2, b2)

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
        self.pixels = self.image.load()

    def edge_detection(self):
        self.image = self.image.filter(ImageFilter.FIND_EDGES)
        self.pixels = self.image.load()

    def reset_image(self):
        """
        Sets the ImageProcessing image back to the default, i.e., the image which the ImageProcessing object was
        instantiated with
        :return: None
        """
        self.image = self.IMAGE_BACKUP.copy()
        self.pixels = self.image.load()

    def fit_to_screen(self, screen_width=1280, screen_height=720):
        """
        Resizes the image to fit on the screen.  Also changes the backup of the original image to this resized image.
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
