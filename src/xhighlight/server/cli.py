import argparse

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from xhighlight.server import server
from xhighlight.util import ensure_screen_composited


argparser = argparse.ArgumentParser(
    description="DBus server for xhighlight (usually invoked automatically)."
)

argparser.add_argument(
    '--opacity', '-o',
    type=float,
    default=.6,
    help="Opacity of the dim overlay (0 ≤ o ≤ 1), where 1 is perfectly opaque."
)


def console_entry():

    ensure_screen_composited()
    args = argparser.parse_args()
    server(args.opacity)
