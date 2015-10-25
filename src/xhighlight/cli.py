import argparse
import signal

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from keybinder.keybinder_gtk import KeybinderGtk

from xhighlight.dimmed import Dimmed
from xhighlight.util import surround_region


parser = argparse.ArgumentParser(
    description="Highlight a region of the screen."
)

parser.add_argument(
    'x',
    type=int,
    help="x coordinate of the region’s upper left corner"
)
parser.add_argument(
    'y',
    type=int,
    help="y coordinate of the region’s upper left corner"
)
parser.add_argument(
    'width',
    type=int,
    help="Region width"
)
parser.add_argument(
    'height',
    type=int,
    help="Region height"
)
parser.add_argument(
    '--opacity', '-o',
    type=float,
    default=.8,
    help="Opacity of the dim overlay (0 ≤ o ≤ 1), where 1 is perfectly opaque."
)


def console_entry():

    args = parser.parse_args()

    for rect in surround_region(args.x, args.y, args.width, args.height):
        Dimmed(*rect, opacity=args.opacity)

    keybinder = KeybinderGtk()
    keybinder.register('<Ctrl>Escape', Gtk.main_quit)
    keybinder.start()

    # Work around bug 622084.
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    Gtk.main()
