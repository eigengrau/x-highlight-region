x-highlight-region
==================

x-highlight-region dims everything but selected regions of the screen. It is
meant to be of use when giving presentations or when recording screencasts.
`Demo video <https://youtu.be/_-tczhQAHo0>`__.


Usage
-----

x-highlight-region may be invoked as specified below. To disengage, press
*C-Esc*.

::

   usage: xhighlight [-h] [--opacity OPACITY] [[r|e]w×h+x+y [[r|e]w×h+x+y ...]]

   Highlight regions of the screen.

   positional arguments:
     [r|e]w×h+x+y          A region specification 'e' for ellipsoid highlights,
                           'r' for rectangular highlights. If the type is not
                           supplied, assume 'r'.

   optional arguments:
     -h, --help            show this help message and exit
     --opacity OPACITY, -o OPACITY
                           Opacity of the dim overlay (0 ≤ o ≤ 1), where 1 is
                           perfectly opaque.


Regions intended for highlighting can be conveniently selected using `slop
<https://github.com/naelstrof/slop>`__:

::

   alias xhl='xhighlight $(slop -f %g)'

To conveniently trigger highlighting via a global keyboard-shortcut, please
refer to a hotkey daemon such as `sxhkd
<https://github.com/baskerville/sxhkd>`__.

Regions can be selected incrementally. When the first invocation has not been
disengaged, further calls to `xhighlight` will add new highlighted regions to
earlier ones.


Requirements
------------

x-highlight-region relies on Gtk+ 3, pycairo, pygobject, and `python3-keybinder
<https://github.com/LiuLang/python3-keybinder>`__. It can be installed as
customary, either by invoking ``setup.py``, or using ``pip``.
