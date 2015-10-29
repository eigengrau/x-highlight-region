"""A semi-transparent Gtk window useful to dim the brightness of regions on the
screen.

"""

import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from xhighlight.util import make_mouse_pass_through


class Dimmed (Gtk.Window):

    def __init__(self, opacity=.8):
        """A semi-transparent screen overlay which supports masking out clear
        regions.

        """

        super().__init__(Gtk.WindowType.POPUP)

        # Be transparent.
        self.set_app_paintable(True)
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        self.set_visual(visual)
        self.show_all()

        # Set geometry.
        width, height = screen.get_width(), screen.get_height()
        self.resize(width, height)
        self.move(0, 0)

        # Make the window not look like a regular window.
        self.fullscreen()
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.set_type_hint(Gdk.WindowTypeHint.NOTIFICATION)

        # Don’t take focus.
        self.set_accept_focus(False)
        self.set_focus_on_map(False)
        make_mouse_pass_through(self)

        # We manage highlighted regions by masking out parts of a completely
        # dimmed, screen-sized overlay.
        overlay = Gtk.Fixed()
        overlay.connect('draw', self._draw_dim)
        self.add(overlay)
        overlay.show_all()
        make_mouse_pass_through(overlay)
        self.overlay = overlay
        self.opacity = opacity

    def add_clear(self, x, y, width, height):
        """Clear a region."""

        frame = Gtk.Frame()
        frame.set_size_request(width, height)
        frame.connect('draw', self._draw_clear)
        self.overlay.put(frame, x, y)
        frame.show_all()
        make_mouse_pass_through(frame)

    def _draw_dim(self, _wid, ctx):

        ctx.set_source_rgba(0, 0, 0, self.opacity)
        ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.paint()

    def _draw_clear(self, _wid, ctx):

        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.paint()
