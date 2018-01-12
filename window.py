#!/usr/bin/env python3
# window.py
from tkinter import Frame
from tkinter import Canvas
from tkinter import ALL, NW, HORIZONTAL
from tkinter import Tk
from tkinter import Toplevel
from tkinter import Message
from tkinter import Button
from tkinter import Menu
from tkinter import Entry
from tkinter import OptionMenu, StringVar
from tkinter import Scale
from PIL import Image, ImageTk
from image_processing_optimized import ImageProcessor

__author__ = 'Seth Tinglof'
__version__ = '1.0'


class Window:

    def __init__(self):
        self.root = Tk()
        self.root.title("Image Processing")
        self.image_frame = Frame(self.root)
        self.canvas = Canvas(self.image_frame)
        self.canvas.pack()
        self.options_frame = Frame(self.root)
        self.options_frame.pack(side='top')
        self.image_frame.pack()
        self.image = None
        self.image_processor = ImageProcessor
        self.tkImage = None
        self.mode = 'none'
        self.current_option = "Reset Image"
        self.create_menu_bar()
        self.root.after(100, self.run_top_level_windows)
        self.root.mainloop()

    def run_top_level_windows(self):
        """
        Creates top level window which describes the application's function to the user.
        :return: None
        """
        self.root.withdraw()
        top = Toplevel()
        top.title("About image processing application.")
        message = Message(top, text="This application is used to process image files.  Begin by hitting Open Image "
                                    "under Options on the title bar and entering the name of a file stored in the "
                                    "images folder.", width=300)
        message.pack()

        def button_hit():
            """
            Actions for when the continue button on the top level window is hit.
            :return: None
            """
            top.destroy()
            self.root.deiconify()
            w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry("%dx%d+0+0" % (w, h))

        button = Button(top, text='continue', command=button_hit)
        button.pack()

    def create_menu_bar(self):
        """
        Adds items to the title bar at the top left of the screen. The user can use these to switch between different
        functions of the application or to exit.
        :return: None
        """
        self.menubar = Menu(self.root)

        # create a pulldown menu, and add it to the menu bar
        self.option_menu = Menu(self.menubar, tearoff=0)
        self.option_menu.add_command(label="Open Image", command=self.open_image_option)
        self.option_menu.add_command(label="Image Processing", command=self.image_processing_option)
        self.option_menu.add_separator()
        self.option_menu.add_command(label="Save", command=self.save)
        self.option_menu.add_command(label="Exit", command=quit)
        self.menubar.add_cascade(label="Options", menu=self.option_menu)
        self.root.config(menu=self.menubar)

    def open_image_option(self):
        """
        Actions taken when user selects to open an image in the application.
        :return: None
        """
        self.cleanup_option_frame()
        self.mode = 'open image'
        self.entry = Entry(self.options_frame)
        self.entry.pack(side='left')

        def set_image():
            """
            Sets the application to the user's selected image
            :return: None
            """
            self.set_image(self.entry.get())
            self.cleanup_option_frame()
            self.mode = 'none'

        self.get_image_button = Button(self.options_frame, text="Get Image", command=set_image)
        self.get_image_button.pack(side='left')

    def image_processing_option(self):
        """
        Actions when user selects the image processing option.  Allows user to change between and execute the different
        image processing operations.
        :return: None
        """
        self.cleanup_option_frame()
        if self.image is None:
            return
        self.mode = 'image processing'
        self.var = StringVar(self.options_frame)
        self.var.set("Reset Image")
        self.options = OptionMenu(self.options_frame, self.var, "Reset Image", "Tint Color", "Trace Edges", "Re-size",
                                  "Grayscale", "Black and White", "Change Saturation", "Invert Color", "Average Color",
                                  "Sepia Tone")
        self.options.pack(side="left")

        def option_selected(*_):
            """
            Switches to the type of image processing that the user selected.
            :param _: Unused parameter, necessary to make function a callback for a Stringvar.
            :return: None
            """
            self.cleanup_image_processing_options()
            if self.var.get() == "Reset Image":
                self.current_option = "Reset Image"
                self.image_processor.reset_image()
                self.update_image()
            elif self.var.get() == "Tint Color":
                self.current_option = "Tint Color"
                self.var2 = StringVar(self.options_frame)
                self.var2.set("Red")
                self.color_options = OptionMenu(self.options_frame, self.var2, "Red", "Orange", "Yellow", "Green",
                                                "Blue", "Cyan", "Magenta", "Violet")
                self.color_options.pack(side='left')

                def change_color(*_):
                    """
                    Tints the image the color that the user selects.
                    :param _: Unused. Necessary to make function a callback function
                    :return:
                    """
                    self.image_processor.color_filter(self.var2.get())
                    self.update_image()

                self.var2.trace('w', change_color)

            elif self.var.get() == "Trace Edges":
                self.current_option = "Trace Edges"
                self.image_processor.edge_detection()
                self.update_image()

            elif self.var.get() == "Re-size":
                self.current_option = "Re-size"
                self.scale = Scale(self.options_frame, from_=.1, to=3, orient=HORIZONTAL, resolution=.1)
                self.scale.pack(side='left')

                def resize():
                    """
                    Re-sizes image by multiplying the dimensions by the user's input scale factor.
                    :return: None
                    """
                    self.image_processor.resize(self.scale.get())
                    self.update_image()

                self.scale_button = Button(self.options_frame, text='Scale', command=resize)
                self.scale_button.pack(side='left')

            elif self.var.get() == "Grayscale":
                self.current_option = "Grayscale"
                self.image_processor.convert_to_grayscale()
                self.update_image()

            elif self.var.get() == "Black and White":
                self.current_option = "Black and White"
                self.image_processor.convert_to_black_and_white()
                self.update_image()

            elif self.var.get() == "Change Saturation":
                self.current_option = "Change Saturation"
                self.scale = Scale(self.options_frame, from_=0, to=2, orient=HORIZONTAL, resolution=.1)
                self.scale.pack(side='left')

                def change_saturation():
                    """
                    Modifies the saturation by the user's input modification factor.
                    :return: None
                    """
                    self.image_processor.modify_saturation(self.scale.get())
                    self.update_image()

                self.scale_button = Button(self.options_frame, text="Change Saturation", command=change_saturation)
                self.scale_button.pack()

            elif self.var.get() == "Invert Color":
                self.current_option = "Invert Color"
                self.image_processor.invert_colors()
                self.update_image()

            elif self.var.get() == "Average Color":
                self.current_option = "Average Color"
                self.image_processor.average_pixel_color()
                self.update_image()

            elif self.var.get() == "Sepia Tone":
                self.current_option = "Sepia Tone"
                self.image_processor.sepia_tone()
                self.update_image()

        self.var.trace("w", option_selected)

    def cleanup_option_frame(self):
        """
        Removes widgets from option frame.
        :return: None
        """
        if self.mode == "open image":
            self.entry.destroy()
            self.get_image_button.destroy()
        elif self.mode == "image processing":
            self.options.destroy()
            self.cleanup_image_processing_options()

    def cleanup_image_processing_options(self):
        """
        Removes widgets used for specific image processing options.
        :return: None
        """
        if self.current_option == "Tint Color":
            self.color_options.destroy()
        elif self.current_option == "Re-size" or self.current_option == "Change Saturation":
            self.scale.destroy()
            self.scale_button.destroy()

    def set_image(self, name):
        """
        Loads image from file in the images/ folder.
        :param name: name of file as a String.
        :return: None
        """
        try:
            self.image = Image.open("images/" + name)
        except:
            return
        self.image_processor = ImageProcessor(self.image)
        self.image_processor.fit_to_screen(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        self.update_image()

    def save(self):
        """
        Save current image in images/ folder with the name output.jpg
        :return: None
        """
        self.image.save("images/output.jpg")

    def update_image(self):
        """
        Updates the application to display the current image from the ImageProcessor object.
        :return: None
        """
        self.image = self.image_processor.image
        self.tkImage = ImageTk.PhotoImage(self.image)
        self.update_canvas()

    def update_canvas(self):
        """
        Updates canvas.  Do not call directly, instead call update_image.
        :return: None
        """
        self.canvas.delete(ALL)
        self.canvas.configure(width=self.image.size[0], height=self.image.size[1])
        self.canvas.create_image(0, 0, image=self.tkImage, anchor=NW)
        self.canvas.update()
