# Image-Processor
A simple image processing program written in python 3.

This project uses the tkinter, Pillow, matplotlib, and numpy libraries. Changing the last import statement in the file 'window.py' from "from image_processing_optimized import ImageProcessor" to "from image_processing import ImageProcessor" should remove the need for the matplotlib and numpy libraries but greatly reduces performance. All images are loaded and saved from and to the images directory.
