"""
    PyResizer
    ~~~~~~~~~

    https://github.com/jedie/PyResizer/
    https://pypi.org/project/PyResizer/

    created 2019 by Jens Diemer
    GNU General Public License v3 or later (GPLv3+)
"""
import datetime
import getpass
from pathlib import Path

SETTINGS_FILE = "~/.PyResizer.json"

# for default settings:
USER_NAME = getpass.getuser()
YEAR = datetime.datetime.utcnow().year

KEY_LAST_PATH = "last_path"
KEY_LAST_SETTINGS_NAME = "last_settings_name"
KEY_CONVERT_SETTINGS = "convert_settings"
KEY_SETTINGS_NAME = "settings_name"

DEFAULT_SETTINGS_NAME = "default"

DEFAULT_SETTINGS = {
    #
    # file path from last open image file:
    KEY_LAST_PATH: Path("~").expanduser(),
    #
    # The last used convert settings:
    KEY_LAST_SETTINGS_NAME: DEFAULT_SETTINGS_NAME,
    #
    # The convert settings:
    KEY_CONVERT_SETTINGS: {
        DEFAULT_SETTINGS_NAME: {
            "filesize": 1000000,
            "max_height": 1000,
            "max_width": 2000,
            "text": "DEFAULT copyright %s by %s (CC BY-NC-ND 2.0)" % (YEAR, USER_NAME),
        },
        "small": {
            "filesize": 200000,
            "max_height": 450,
            "max_width": 600,
            "text": "SMALL copyright %s by %s (CC BY-NC-ND 2.0)" % (YEAR, USER_NAME),
        },
    },
}

# For open image dialog:
IMAGE_FILE_MASK = ("*.jpg", "*.jpeg", "*.png", "*.dng", "*.DNG")
