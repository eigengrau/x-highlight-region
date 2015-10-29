import signal
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from keybinder.keybinder_gtk import KeybinderGtk

from xhighlight.dimmed import Dimmed
from xhighlight.cli.parse import argparser, parse_region_spec


def console_entry():

    args = argparser.parse_args()

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
