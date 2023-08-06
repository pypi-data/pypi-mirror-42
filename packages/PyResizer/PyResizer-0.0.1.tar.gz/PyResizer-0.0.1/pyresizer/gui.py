#!/usr/bin/env python3

"""
    PyResizer
    ~~~~~~~~~

    https://github.com/jedie/PyResizer/
    https://pypi.org/project/PyResizer/

    created 2019 by Jens Diemer
    GNU General Public License v3 or later (GPLv3+)
"""
import copy
import json
import logging
import sys
import tempfile
from pathlib import Path
from pprint import pprint

from pyresizer.constants import (
    DEAFULT_CONVERT_KEY, DEFAULT_SETTINGS, IMAGE_FILE_MASK, KEY_CONVERT_SETTINGS, KEY_LAST_PATH, KEY_SETTINGS_NAME,
    SETTINGS_FILE
)
from pyresizer.image import convert
from pyresizer import __version__

try:
    import tkinter as tk
    from tkinter import messagebox, ttk, filedialog
    from tkinter.scrolledtext import ScrolledText
except ImportError as err:
    print("\nERROR can't import Tkinter: %s\n" % err)
    print("Hint: 'apt install python3-tk'\n")
    sys.exit(-1)


log = logging.getLogger(__name__)

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as err:
    print("ERROR: %s" % err)
    print("Install https://python-pillow.org/ !")
    print("pip install Pillow")
    sys.exit(-1)


def get_tk_photo_image(file_path, size=(600, 300)):
    print("Open image: %s" % file_path)
    with tempfile.NamedTemporaryFile(suffix=".ppm") as f:
        log.debug("create temp file: %s", f.name)

        im_temp = Image.open(str(file_path))
        print("Origin image size: %i x %i px" % im_temp.size)

        im_temp.thumbnail(size, Image.ANTIALIAS)

        im_temp.save(f.name, "ppm")

        photo = tk.PhotoImage(file=f.name)
    return photo


class JSONEncoder(json.JSONEncoder):
    """
    Just convert Path() instance to strings
    """

    def default(self, obj):
        if isinstance(obj, Path):
            return str(obj)

        return json.JSONEncoder.default(self, obj)


class ImageResizeGui(tk.Tk):
    def __init__(self, width=800):
        super().__init__()
        self.geometry(
            "%dx%d+%d+%d"
            % (
                width,
                self.winfo_screenheight() * 0.6,
                (self.winfo_screenwidth() - width) / 2,
                self.winfo_screenheight() * 0.1,
            )
        )
        self.set_title("loading...")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.settings_path = Path(SETTINGS_FILE).expanduser()
        self.preferences = None

        if self.settings_path.is_file():
            print("Load settings from: %s" % self.settings_path)
            with self.settings_path.open("r") as f:
                try:
                    self.preferences = json.load(f)
                except Exception as err:
                    log.exception("Can't read json: %s" % err)
                    print("ERROR: %s" % err)
        else:
            print("No settings file: %s" % self.settings_path)

        if self.preferences:
            # "validate" loaded settings

            if KEY_LAST_PATH not in self.preferences:
                self.preferences = None
            elif KEY_CONVERT_SETTINGS not in self.preferences:
                self.preferences = None
            else:
                if DEAFULT_CONVERT_KEY not in self.preferences[KEY_CONVERT_SETTINGS]:
                    self.preferences = None

            if self.preferences is None:
                print("ERROR in %s, ignore file content" % self.settings_path)

        if self.preferences is None:
            print("Use default settings")
            self.preferences = DEFAULT_SETTINGS

        self.last_path = self.preferences[KEY_LAST_PATH]
        self.current_image_path = None

        print("\nAll settings:")
        pprint(self.preferences)

        self.current_settings_key = DEAFULT_CONVERT_KEY
        self.current_settings = self._init_current_settings()

        print("\nCurrent 'default' settings:")
        pprint(self.current_settings)

        ####################################################################################
        # main frame: image preview
        main_row = 0

        self.image_preview_frame = ttk.Frame(self, padding="5 5 5 5")
        self.image_preview_frame.grid(row=main_row, column=0, sticky=tk.NSEW)
        self.image_preview_frame.columnconfigure(0, weight=1)
        self.image_preview_frame.rowconfigure(0, weight=1)

        frame_row = 0

        self.image_preview = tk.Label(self.image_preview_frame)
        self.image_preview.grid(row=frame_row, column=0, sticky=tk.NSEW)

        frame_row += 1

        self.label_image_preview = ttk.Label(self.image_preview_frame, text="")
        self.label_image_preview.grid(row=frame_row, column=0, sticky=tk.EW)

        ####################################################################################
        # main frame: input fields
        main_row += 1

        self.label_frame = ttk.Frame(self, padding="5 5 5 5")
        self.label_frame.grid(row=main_row, column=0, sticky=tk.NSEW)

        frame_row = 0

        self.label_text = ttk.Label(self.label_frame, text="copyright text:")
        self.label_text.grid(row=frame_row, column=0, sticky=tk.NSEW)
        self.entry_text = ttk.Entry(self.label_frame, width=50, textvariable=self.current_settings["text"])
        self.entry_text.grid(row=frame_row, column=1, sticky=tk.W)

        frame_row += 1

        self.label_filesize = ttk.Label(self.label_frame, text="max file size:")
        self.label_filesize.grid(row=frame_row, column=0, sticky=tk.NSEW)
        self.entry_filesize = ttk.Entry(self.label_frame, width=7, textvariable=self.current_settings["filesize"])
        self.entry_filesize.grid(row=frame_row, column=1, sticky=tk.W)

        frame_row += 1

        self.label_max_width = ttk.Label(self.label_frame, text="image max. width:")
        self.label_max_width.grid(row=frame_row, column=0, sticky=tk.NSEW)
        self.entry_max_width = ttk.Entry(self.label_frame, width=5, textvariable=self.current_settings["max_width"])
        self.entry_max_width.grid(row=frame_row, column=1, sticky=tk.W)

        frame_row += 1

        self.label_max_height = ttk.Label(self.label_frame, text="image max. height:")
        self.label_max_height.grid(row=frame_row, column=0, sticky=tk.NSEW)
        self.entry_max_height = ttk.Entry(self.label_frame, width=5, textvariable=self.current_settings["max_height"])
        self.entry_max_height.grid(row=frame_row, column=1, sticky=tk.W)

        frame_row += 1

        self.label_load_settings = ttk.Label(self.label_frame, text="load settings:")
        self.label_load_settings.grid(row=frame_row, column=0, sticky=tk.NSEW)
        self.entry_load_settings = ttk.Combobox(self.label_frame, width=20, textvariable=tk.StringVar())
        self.entry_load_settings["values"] = tuple(self.preferences[KEY_CONVERT_SETTINGS].keys())
        self.entry_load_settings.bind("<<ComboboxSelected>>", self.load_settings)
        self.entry_load_settings.grid(row=frame_row, column=1, sticky=tk.W)

        frame_row += 1

        self.button_save_settings = tk.Button(
            self.label_frame, text="Create new settings:", command=self.new_convert_settings
        )
        self.button_save_settings.grid(row=frame_row, column=0, sticky=tk.NSEW)
        self.entry_settings_name = ttk.Entry(
            self.label_frame, width=20, textvariable=self.current_settings["settings_name"]
        )
        self.entry_settings_name.grid(row=frame_row, column=1, sticky=tk.W)

        ####################################################################################
        # main frame: action buttons
        main_row += 1

        self.action_frame = ttk.Frame(self, padding="5 5 5 5")
        self.action_frame.grid(row=main_row, column=0, sticky=tk.NSEW)
        # self.action_frame.columnconfigure(0, weight=1)
        # self.action_frame.rowconfigure(0, weight=1)

        self.button_ask_open_file = tk.Button(
            self.action_frame, text="Open Image", command=self.callback_ask_open_file
        )
        self.button_ask_open_file.grid(row=0, column=0, sticky=tk.NSEW)

        self.action_button = tk.Button(self.action_frame, text="Convert", command=self.callback_convert)
        self.action_button.grid(row=0, column=1, sticky=tk.NSEW)

        self.action_button_quit = tk.Button(self.action_frame, text="Quit", command=self.destroy)
        self.action_button_quit.grid(row=0, column=2, sticky=tk.NSEW)

        ####################################################################################
        # main frame: info scrolled text box
        main_row += 1

        self.info_text = ScrolledText(self, bg="white", height=10)
        self.info_text.grid(row=main_row, column=0, sticky=tk.NSEW)
        self.info_text.columnconfigure(0, weight=1)
        self.info_text.rowconfigure(0, weight=1)

        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=2)

        self.origin_stdout_write = sys.stdout.write
        sys.stdout.write = self.stdout_redirect_handler

        self.set_preview_image(
            file_path=Path(
                # "/home/jens/Bilder/K5II2357.jpg"
                "/home/jens/windows_daten/Bilder/Bilder/2019/02/24/K1__0140_klein.jpg"
            )
        )

        self.mainloop()

    def _init_current_settings(self):
        data = self.preferences[KEY_CONVERT_SETTINGS][self.current_settings_key]
        new_settings = data.copy()
        new_settings[KEY_SETTINGS_NAME] = self.current_settings_key

        for key, value in new_settings.items():
            try:
                value = int(value)
            except ValueError:
                obj = tk.StringVar
            else:
                obj = tk.IntVar

            instance = obj(master=self, value=value, name=key)
            new_settings[key] = instance

        pprint(new_settings)
        return new_settings

    def _current_settings2preferences(self):
        settings_name = self.entry_settings_name.get()
        print("Save settings to:", settings_name)

        if settings_name not in self.preferences[KEY_CONVERT_SETTINGS]:
            print("Save new settings to: %r" % settings_name)
            self.preferences[KEY_CONVERT_SETTINGS][settings_name] = {}

        for key, value in self.current_settings.items():
            self.preferences[KEY_CONVERT_SETTINGS][settings_name][key] = value.get()

        self.preferences[KEY_LAST_PATH] = self.last_path

        pprint(self.preferences[KEY_CONVERT_SETTINGS][settings_name])

    def load_settings(self, *args):
        settings_name = self.entry_load_settings.get()
        print("\nLoad settings:", settings_name)

        new_settings = self.preferences[KEY_CONVERT_SETTINGS][settings_name]
        pprint(new_settings)

        for key, value in new_settings.items():
            tk_variable = self.current_settings[key]
            print(repr(tk_variable), repr(value))
            tk_variable.set(value)

        self.current_settings[KEY_SETTINGS_NAME].set(settings_name)

    def new_convert_settings(self):
        self._current_settings2preferences()

    def save_settings(self):
        """
        Save current settings into: "~/.PyResizer.json"
        """
        self._current_settings2preferences()

        print("Save settings to: %s" % self.settings_path)
        pprint(self.preferences)

        temp = copy.deepcopy(self.preferences)
        for convert_settings in temp[KEY_CONVERT_SETTINGS].values():
            if KEY_SETTINGS_NAME in convert_settings:
                del (convert_settings[KEY_SETTINGS_NAME])

        with self.settings_path.open("w") as f:
            json.dump(temp, f, indent="\t", cls=JSONEncoder)

    def set_title(self, text):
        self.title("%s v%s - %s" % (self.__class__.__name__, __version__, text))

    def set_preview_image(self, file_path):
        self.current_image_path = file_path.parent
        self.set_title(str(file_path))
        self.label_image_preview.configure(text=str(file_path))

        self.photo = get_tk_photo_image(file_path=file_path, size=(600, 300))
        self.image_preview.configure(image=self.photo)
        self.image_preview.image = self.photo
        log.debug("New image set: %s", self.image_preview.image)

    def callback_ask_open_file(self, *args):
        print("_" * 100)
        print("Use current path:", self.current_image_path)
        filename = filedialog.askopenfilename(
            initialdir=str(self.current_image_path),
            title="Select image to resize",
            filetypes=[("Images", IMAGE_FILE_MASK), ("all files", "*.*")],
        )
        if not filename:
            print("No file selected, ok")
            return

        self.set_preview_image(file_path=Path(filename))

    def callback_convert(self, *args):
        print("Convert:", self.current_image_path)

        text = self.entry_text.get()
        print("Text: %r" % text)

        max_size = int(self.entry_filesize.get())
        print("Max file size: %i Bytes" % max_size)

        max_width = int(self.entry_max_width.get())
        max_height = int(self.entry_max_height.get())
        size = (max_width, max_height)
        print("Max image size: %i x %i Pixels" % size)

        convert(
            file_path=self.current_image_path,
            out_prefix="_small",
            overwrite_existing=True,
            size=size,
            #
            # https://github.com/python-pillow/Pillow/tree/master/Tests/fonts
            # font_path="Pillow/Tests/fonts/FreeMono.ttf",
            font_path="Pillow/Tests/fonts/DejaVuSans.ttf",
            # font_path="/usr/share/fonts/truetype",
            #
            text=text,  # ,
            text_opacity=70,
            max_size=max_size,
            quality=99,
            quality_steps=1,
        )

        self.save_settings()  # Save current settings into: "~/.PyResizer.json"

    def output_callback(self, text):
        self.info_text.insert(tk.END, "%s\n" % text)
        self.info_text.see(tk.END)

    def stdout_redirect_handler(self, *args):
        self.origin_stdout_write(*args)

        text = " ".join([str(part) for part in args])
        self.info_text.insert(tk.END, text)
        self.info_text.see(tk.END)

    def destroy(self, *args):
        close = messagebox.askyesno(title="close?", message="Quit?")
        if close:
            self.save_settings()  # Save current settings into: "~/.PyResizer.json"
            super().destroy()


def main():
    gui = ImageResizeGui(width=800)


if __name__ == "__main__":
    main()
