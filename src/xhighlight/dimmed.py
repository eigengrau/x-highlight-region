"""A semi-transparent Gtk window useful to dim the brightness of regions on the
screen.

"""

import math

import cairo
from gi.repository import Gtk, Gdk

from xhighlight.region import Region, Shape


class Dimmed (Gtk.Window):

    def __init__(self, opacity=.6):
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
        self.input_shape_combine_region(cairo.Region())

        # Keep state.
        self._regions = []
        self.opacity = opacity

        self.connect('draw', self._on_draw)

    def _on_draw(self, _wid, ctx):

        ctx.save()

        # Dim everything.
        ctx.set_source_rgba(0, 0, 0, self.opacity)
        ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.paint()

        # Process highlighted regions.
        ctx.set_operator(cairo.OPERATOR_CLEAR)
        for region in self._regions:

            if region.shape == Shape.rectangular:

                ctx.rectangle(
                    region.x,
                    region.y,
                    region.width,
                    region.height
                )
                ctx.fill()

            elif region.shape == Shape.ellipsoid:

                ctx.save()
                ctx.translate(
                    region.x+region.width/2,
                    region.y+region.height/2
                )
                ctx.scale(region.width/2, region.height/2)
                ctx.arc(0, 0, 1, 0, math.radians(360))
                ctx.fill()
                ctx.restore()

            else:

                raise ValueError(
                    "Don’t know how to process region: %s" % region
                )

        ctx.restore()

    def clear_region(self, region):
        """Highlight a region on the screen."""

        self._regions.append(region)
        self.queue_draw()
