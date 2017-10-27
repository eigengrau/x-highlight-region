import sys
from ctypes import cdll

from gi.repository import Gdk


def ensure_screen_composited():

    root = Gdk.get_default_root_window()
    screen = root.get_screen()
    if not screen.is_composited():
        print("This program requires a composited screen.")
        sys.exit(1)
