Mathematical rounding in Python 3
=================================


This package is designed for using mathematical rounding. This type of rounding was used by function - round () in python 2.

Quick start
===========

#. Install this package using pip::

    pip install math-round

#. Import **mround** function from **math_round** package.
#. Use like this::

    mround(12.123) # - > 12
    mround(12.123, 1) # -> 12.1
#. To replace the standard function - round () in the whole project, write the following in the main __init__ file:

::

    import builtins
    from math_round import mround


    builtins.round = mround
