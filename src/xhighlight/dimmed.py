"""A semi-transparent Gtk window useful to dim the brightness of regions on the
screen.

"""

from ctypes import cdll

import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class Dimmed (Gtk.Window):

    def __init__(self, x, y, width, height, opacity=.8):
        """A semi-transparent Gtk window useful to dim the brightness of regions
        of the screen.

        """

        super().__init__(Gtk.WindowType.POPUP)
        self.opacity = opacity

        self.connect('draw', self.on_draw)

        # Be transparent.
        self.set_app_paintable(True)
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        self.set_visual(visual)

        # Set geometry.
        self.resize(width, height)
        self.move(x, y)

        # Make the window not look like a regular window.
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.set_type_hint(Gdk.WindowTypeHint.NOTIFICATION)

        # Don’t take focus.
        self.set_accept_focus(False)
        self.set_focus_on_map(False)

        self.show_all()

        # Make our window completely transparent to mouse events. pycairo
        # doesn’t seem to support interfacing Cairo regions with Gtk, so we
        # hackishly set the input shape using native calls. This relies on
        # __hash__ yielding the pointer to the native structure of Gdk windows.
        libgdk = cdll.LoadLibrary('libgdk-3.so')
        libcairo = cdll.LoadLibrary('libcairo.so')
        window = self.get_window()
        window_pointer = hash(window)
        region_pointer = libcairo.cairo_region_create()
        offset = 0, 0
        libgdk.gdk_window_input_shape_combine_region(
            window_pointer,
            region_pointer,
            *offset
        )

    def on_draw(self, _wid, ctx):

        ctx.set_source_rgba(0, 0, 0, self.opacity)
        ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.paint()
