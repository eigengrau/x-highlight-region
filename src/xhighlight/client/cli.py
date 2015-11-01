import argparse

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from xhighlight.client import client
from xhighlight.parsing import RegionAction
from xhighlight.region import Region, Shape
from xhighlight.util import ensure_screen_composited


argparser = argparse.ArgumentParser(
    description="Highlight regions on the screen."
)

argparser.add_argument(
    '--rectangle', '-r',
    dest='rectangles',
    nargs=4,
    type=int,
    action=RegionAction,
    shape=Shape.rectangular,
    help="highlight a rectangular region (may occur multiple times)"
)

argparser.add_argument(
    '--ellipsis', '-e',
    dest='ellipsoids',
    nargs=4,
    type=int,
    action=RegionAction,
    shape=Shape.ellipsoid,
    help="highlight an ellipsoid region (may occur multiple times)"
)

argparser.add_argument(
    '--opacity', '-o',
    default=.8,
    type=float,
    help="opacity of the dim overlay (0 ≤ o ≤ 1), where 1 is perfectly opaque"
)


def console_entry():

    ensure_screen_composited()
    args = argparser.parse_args()
    highlight_regions = args.rectangles + args.ellipsoids
    client(highlight_regions, args.opacity)
