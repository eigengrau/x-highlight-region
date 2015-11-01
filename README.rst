x-highlight-region
==================

x-highlight-region dims everything but selected regions on the screen. It is
meant to be of use when giving presentations or when recording screencasts.


.. image:: http://i.imgur.com/vt7koWb.gif
   :target: https://youtu.be/_-tczhQAHo0


Usage
-----

x-highlight-region may be invoked as specified below. To disengage, press
*C-Esc*.

::

   usage: xhighlight [-h] [--rectangle X Y WIDTH HEIGHT]
                     [--ellipsis X Y WIDTH HEIGHT] [--clear] [--opacity OPACITY]

   Highlight regions on the screen.

   optional arguments:
     -h, --help            show this help message and exit
     --rectangle X Y WIDTH HEIGHT, -r X Y WIDTH HEIGHT
                           highlight a rectangular region (may occur multiple
                           times)
     --ellipsis X Y WIDTH HEIGHT, -e X Y WIDTH HEIGHT
                           highlight an ellipsoid region (may occur multiple
                           times)
     --clear, -c           clear everything
     --opacity OPACITY, -o OPACITY
                           opacity of the dim overlay (0 ≤ o ≤ 1), where 1 is
                           perfectly opaque

Regions intended for highlighting can be conveniently selected using `slop
<https://github.com/naelstrof/slop>`__:

::

   alias xhl='xhighlight -r $(slop -f "%x %y %w %h")'

To conveniently trigger highlighting via a global keyboard-shortcut, please
refer to a hotkey daemon such as `sxhkd
<https://github.com/baskerville/sxhkd>`__.

Regions can be selected incrementally. When the first invocation has not been
disengaged, further calls to `xhighlight` will add new highlighted regions to
earlier ones.


Requirements
------------

x-highlight-region relies on Gtk+ 3, pycairo, pygobject, python-dbus, and
`python3-keybinder <https://github.com/LiuLang/python3-keybinder>`__. It can be
installed as customary, either by invoking ``setup.py``, or using ``pip``. Since
pygobject, python-dbus, and pycairo are not distributed via pypi, these must be
installed via your distribution’s package manager.
