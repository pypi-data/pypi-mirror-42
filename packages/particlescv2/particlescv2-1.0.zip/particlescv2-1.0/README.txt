============
particlescv2
============

particlescv2 is a port of the Particles Python PyGame library PyIgniton for
OpenCV2. The original PyIgntion files can be found at 
`https://launchpad.net/pyignition <https://launchpad.net/pyignition>`_. 

The original repository for particlescv2 is at:
`Github <https://github.com/bunkahle/particlescv2>`_.

Setup the library by running setup_cython.py::

    setup_cython.py build_ext --inplace

This will generate a compiled cythonized particlescv2.pyd (Windows) or particlescv2.so (Linux, Mac)
from the file particlescv2.pyx. This is useful for speed and performance.
particlescv2 seems to be even faster than the original PyGame library PyIgnition.

The library is pretty fast even if it is not compiled. The plain Python 
routine can be found in particlescv2.py. 

Binary for Win-32 Python27
==========================
For convenience there is also the precompiled binary for Win-32 Python 2.7
included: particlescv2.pyd. Copy this file to Lib/site-packages directory
and you are ready to go::

    import particlescv2
    ... your code

Examples
========
There are several examples for running the library in the Examples section.

Requirements
============
The code currently only runs under Python 2.7. Ports to Python 3 are welcome.
If you want to compile the pyx file with cython you also need cython of course.
The blist is required for running as well as numpy and opencv2.
These libraries can easily be installed with
pip install numpy
pip install blist
pip install opencv-python

optionally
pip install cython

opencv2 and numpy windows binaries and setup wheels can also be downloaded from
Christoph Gohlkes Python page for windows:
https://www.lfd.uci.edu/~gohlke/pythonlibs/

License
=======
Same license as PyIgntion: GNU GPL v3 
