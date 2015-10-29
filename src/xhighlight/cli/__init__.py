import os
import signal
import sys
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib
from keybinder.keybinder_gtk import KeybinderGtk

from xhighlight.dimmed import Dimmed
from xhighlight.cli.parse import argparser, parse_region_specs
from xhighlight.cli.server import server
from xhighlight.cli.client import client


def console_entry():

    args = argparser.parse_args()
    highlight_regions = parse_region_specs(args)

    control_path = os.path.join(
        GLib.get_user_runtime_dir(),
        'xhighlight-control'
    )

    if os.path.exists(control_path):

        client(control_path, highlight_regions)

    else:

        pid = os.fork()

        if pid == 0:
            server(control_path, args.opacity)

        else:
            # Make sure the FIFO is created by the server, not the client.
            while not os.path.exists(control_path):
                time.sleep(0.1)
            client(control_path, highlight_regions)
