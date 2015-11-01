import signal
import queue

import dbus
import dbus.service
import dbus.mainloop.glib

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, GLib
from keybinder.keybinder_gtk import KeybinderGtk

from xhighlight.dimmed import Dimmed
from xhighlight.region import Region, Shape


def server(opacity):

    dimmed = Dimmed(opacity)

    keybinder = KeybinderGtk()
    keybinder.register('<Ctrl>Escape', Gtk.main_quit)
    keybinder.start()

    signal.signal(signal.SIGTERM, Gtk.main_quit)
    signal.signal(signal.SIGINT, Gtk.main_quit)

    ControlReader(dimmed).start()
    Gtk.main()


class ControlReader (dbus.service.Object):

    # Bad things will happen if we call directly into add_clear from a
    # separate thread. So we use a queue instead, which will be read from
    # within the Gtk main loop.

    def __init__(self, dimmed):

        bus = dbus.SessionBus(
            mainloop=dbus.mainloop.glib.DBusGMainLoop()
        )
        bus_name = dbus.service.BusName(
            'net.wirrsal.xhighlight',
            bus
        )
        super().__init__(bus_name, '/')

        self.dimmed = dimmed
        self.read_queue = None

    def start(self):

        self.read_queue = queue.Queue()
        GLib.timeout_add(50, self.mainloop_handle_queue)

    def put(self, item):

        self.read_queue.put(item)

    @dbus.service.method('net.wirrsal.xhighlight')
    def highlight_rectangle(self, x, y, width, height):

        region = Region(Shape.rectangular, x, y, width, height)
        self.put(region)

    @dbus.service.method('net.wirrsal.xhighlight')
    def highlight_ellipsis(self, x, y, width, height):

        region = Region(Shape.ellipsoid, x, y, width, height)
        self.put(region)

    def mainloop_handle_queue(self):

        # Callback used to read the queue from within the Gtk main loop.

        try:
            region = self.read_queue.get_nowait()

        except queue.Empty:
            pass

        else:
            self.dimmed.clear_region(region)

        return True
