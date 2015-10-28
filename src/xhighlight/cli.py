import argparse
import signal
import re
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from keybinder.keybinder_gtk import KeybinderGtk

from xhighlight.dimmed import Dimmed


parser = argparse.ArgumentParser(
    description="Highlight regions of the screen."
)
parser.add_argument(
    'region_specs',
    nargs='+',
    type=str,
    metavar='w×h+x+y',
    help="A region specification (width×height+x+y)."
)
parser.add_argument(
    '--opacity', '-o',
    type=float,
    default=.8,
    help="Opacity of the dim overlay (0 ≤ o ≤ 1), where 1 is perfectly opaque."
)


region_spec_re = re.compile(r"""
    ^
    (?P<width>\d+)
    [×xX]
    (?P<height>\d+)
    \+
    (?P<x>\d+)
    \+
    (?P<y>\d+)
    $
""", re.X)


def parse_region_spec(region_spec):

    parsed = region_spec_re.match(region_spec)

    try:
        return {
            k: int(v)
            for (k, v) in parsed.groupdict().items()
        }

    except (AttributeError, ValueError):
        raise ValueError("Malformed region spec: %s" % region_spec)


def console_entry():

    args = parser.parse_args()

    regions = []
    for region_spec in args.region_specs:

        try:
            region = parse_region_spec(region_spec)

        except ValueError as exc:
            print(exc, file=sys.stderr)
            sys.exit(1)

        else:
            regions.append(region)

    dimmed = Dimmed(opacity=args.opacity)
    for region in regions:

        dimmed.add_clear(
            region['x'],
            region['y'],
            region['width'],
            region['height']
        )

    keybinder = KeybinderGtk()
    keybinder.register('<Ctrl>Escape', Gtk.main_quit)
    keybinder.start()

    # Work around bug 622084.
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    Gtk.main()
