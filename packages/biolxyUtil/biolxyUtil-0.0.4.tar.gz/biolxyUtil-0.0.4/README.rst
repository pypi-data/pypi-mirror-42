==========
biolxyUtil
==========

The is a test version

Installation
============

biolxyUtil runs on Python 2 and Python 3. Your operating system might already provide Python
2.7, which you can check on the command line::

    python --version

If your operating system already includes Python 2.6, I suggest either using
``conda`` (see below) or installing Python 2.7 alongside the existing Python 2.6
instead of attempting to upgrade it in-place. Your package manager might provide
both versions of Python.

To run the recommended segmentation algorithms CBS and Fused Lasso, you will
need to also install the R dependencies (see below).


From a Python package repository
--------------------------------

Reasonably up-to-date biolxyUtil packages are available on `PyPI
<https://pypi.python.org/pypi/biolxyUtil>`_ and can be installed using `pip
<https://pip.pypa.io/en/latest/installing.html>`_ (usually works on Linux if the
system dependencies listed below are installed)::

    pip install biolxyUtil


From source
-----------

The script ``biolxyUtil.py`` requires no installation and can be used in-place. Just
install the dependencies.

To install the main program, supporting scripts and ``cnvlib`` Python library,
use ``setup.py`` as usual::

    python setup.py build
    python setup.py install







