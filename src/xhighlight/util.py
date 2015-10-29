from ctypes import cdll

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk


libgdk = cdll.LoadLibrary('libgdk-3.so')
libcairo = cdll.LoadLibrary('libcairo.so')


def make_mouse_pass_through(widget):
    """Make a widget completely transparent to mouse events."""

    # pycairo doesn’t seem to support interfacing Cairo regions with Gtk, so we
    # hackishly set the input shape using native calls. This relies on __hash__
    # yielding the pointer to the native structure of Gdk windows.

    # Bad things will happen if we proceed with invisible widgets.
    if not widget.is_visible():
        raise ValueError("Widget must be visible.")

    # FIXME Bad things will also happen when the widget is shown, but not yet
    # put() into a container.

    # Dispatch the native call hack.
    window = widget.get_window()
    window_pointer = hash(window)
    region_pointer = libcairo.cairo_region_create()
    offset = 0, 0
    libgdk.gdk_window_input_shape_combine_region(
        window_pointer,
        region_pointer,
        *offset
    )
