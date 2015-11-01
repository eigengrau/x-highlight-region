import sys
import os
import time

import dbus

import xhighlight.server
from xhighlight.region import Shape


def get_server_proxy(block=False):

    bus = dbus.SessionBus()

    while True:

        if bus.name_has_owner('net.wirrsal.xhighlight'):

            server = bus.get_object('net.wirrsal.xhighlight', '/')
            return server

        if not block:

            # python-dbus seems to cache the connection object somehow, and will
            # be unhappy when we fork() later on in client() if the connection
            # isn’t closed.

            bus.close()

            raise dbus.exceptions.DBusException

        # While we could wait for a NameOwnerChange signal to see when the
        # server has appeared, dbus-python wants to use the GLib main loop for
        # this, and odd things will happen when doing so because we used fork().
        # So instead, we poll manually.

        time.sleep(0.1)


def highlight_regions(regions, server_opacity):

    try:

        server = get_server_proxy()

    except dbus.exceptions.DBusException:

        # If no server is running, start one. We could rely on DBus activation,
        # but this would require users to install the service files (which
        # can’t be done automatically by setuptools). Additionally, starting
        # the server from the client allows us to set the server opacity on the
        # client command-line, which would otherwise require a global config
        # file for the server.

        pid = os.fork()

        if pid == 0:

            xhighlight.server.server(server_opacity)
            sys.exit()

        else:

            server = get_server_proxy(block=True)

    for region in regions:

        if region.shape == Shape.rectangular:

            method = server.highlight_rectangle

        elif region.shape == Shape.ellipsoid:

            method = server.highlight_ellipsis

        else:

            raise TypeError("Do not know how to process region: %s" % region)

        method(
            region.x,
            region.y,
            region.width,
            region.height
        )


def server_quit():

    bus = dbus.SessionBus()

    if bus.name_has_owner('net.wirrsal.xhighlight'):

        server = get_server_proxy()
        server.server_quit()
