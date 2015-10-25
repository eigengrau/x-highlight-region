x-highlight-region
==================

x-highlight-region dims everything but a selected region of the screen. It is
meant to be of use when giving presentations or when recording screencasts.
`Demo video <https://youtu.be/t3xBhrYHJlI>`__.


Usage
-----

x-highlight-region may be invoked as specified below. To disengage, press
*C-Esc*.

::

  usage: xhighlight [-h] [--opacity OPACITY] x y w h

  Highlight a region of the screen.

  positional arguments:
    x                     x coordinate of the region’s upper left corner
    y                     y coordinate of the region’s upper left corner
    w                     Region width
    h                     Region height

  optional arguments:
    -h, --help            show this help message and exit
    --opacity OPACITY, -o OPACITY
                          Opacity of the dim overlay (0 ≤ o ≤ 1), where 1 is
                          perfectly opaque.


The region intended for highlighting can be conveniently selected using `slop
<https://github.com/naelstrof/slop>`__:

::

   alias xhl='xhighlight $(slop -f "%x %y %w %h")'

To conventiently trigger highlighting via a global keyboard-shortcut, please
refer to a hotkey daemon such as `sxhkd
<https://github.com/baskerville/sxhkd>`__.


Requirements
------------

x-selection-pipe relies on Gtk+ 3, pygobject, and `python3-keybinder
<https://github.com/LiuLang/python3-keybinder>`__. It can be installed as
customary, either by invoking ``setup.py``, or using ``pip``.
