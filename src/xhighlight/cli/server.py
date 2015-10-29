import os
import signal
import select
import queue
import threading

from gi.repository import Gtk, GLib
from keybinder.keybinder_gtk import KeybinderGtk

from xhighlight.dimmed import Dimmed
from xhighlight.cli.parse import parse_region_spec


def server(control_path, opacity):

    dimmed = Dimmed(opacity)

    keybinder = KeybinderGtk()
    keybinder.register('<Ctrl>Escape', Gtk.main_quit)
    keybinder.start()

    # Work around bug 622084.
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    try:
        os.mkfifo(control_path)
        with open(control_path, 'r') as control:

            control_reader = ControlReader(dimmed, control)
            control_reader.start()

            try:
                Gtk.main()
            finally:
                control_reader.join()

    finally:
        os.remove(control_path)


class ControlReader (threading.Thread):

    # Bad things will happen if we call directly into add_clear from a
    # separate thread. So we use a queue instead, which will be read from
    # within the Gtk main loop.

    def __init__(self, dimmed, control):

        super().__init__(target=self.read_control)

        self.dimmed = dimmed
        self.control = control
        self.read_queue = None
        self.stop_event = None

    def start(self):

        self.stop_event = threading.Event()
        self.read_queue = queue.Queue()
        GLib.timeout_add(50, self.mainloop_handle_queue)

        super().start()

    def put(self, item):

        self.read_queue.put(item)

    def join(self):

        self.stop_event.set()
        super().join()

    def read_control(self, timeout=1):

        while not self.stop_event.is_set():

            ready_read, _, _ = select.select([self.control], [], [], timeout)

            if self.control in ready_read:
                line = self.control.readline()
            else:
                line = None

            if line:
                try:
                    region = parse_region_spec(line)
                except ValueError:
                    pass
                else:
                    self.read_queue.put(region)

    def mainloop_handle_queue(self):

        # Callback used to read the queue from within the Gtk main loop.

        try:
            region = self.read_queue.get_nowait()

        except queue.Empty:
            pass

        else:
            self.dimmed.add_clear(
                region['x'],
                region['y'],
                region['width'],
                region['height']
            )

        return True
