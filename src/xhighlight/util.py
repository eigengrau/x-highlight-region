import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk


def surround_region(x, y, width, height):
    "Return four rectangles which circumscribe the input region."

    screen = Gdk.get_default_root_window().get_screen()
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    top = 0, 0, screen_width, y
    bottom = 0, y+height, screen_width, screen_height-y
    left = 0, y, x, height
    right = x+width, y, screen_width-width, height
    return top, bottom, left, right
