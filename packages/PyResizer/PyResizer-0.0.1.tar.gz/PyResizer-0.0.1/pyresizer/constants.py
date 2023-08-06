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
USER_NAME = getpass.getuser()
YEAR = datetime.datetime.utcnow().year
KEY_LAST_PATH = "last_path"
KEY_CONVERT_SETTINGS = "convert_settings"
KEY_SETTINGS_NAME = "settings_name"
DEAFULT_CONVERT_KEY = "default"
SETTINGS_ATTR_NAMES = ("text", "filesize", "max_width", "max_height")
DEFAULT_SETTINGS = {
    KEY_LAST_PATH: Path("~").expanduser(),
    KEY_CONVERT_SETTINGS: {
        DEAFULT_CONVERT_KEY: {
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
IMAGE_FILE_MASK = ("*.jpg", "*.jpeg", "*.png", "*.dng", "*.DNG")
