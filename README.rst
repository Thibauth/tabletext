Tabletext
=========

``tabletext`` is a Python library to format (pretty-print) tabular data as text
tables. Its goal is to be as simple as possible, while allowing optional
customization of the output.

``tabletext`` also comes with a command line utility, ``table`` which formats
its input into a table and prints it on the standard output.

Installation
------------

``tabletext`` is available on Pypi and can be installed with:

.. code-block:: bash

    $ pip install tabletext

Overview
--------

Library
~~~~~~~

``tabletext`` exposes a single function, ``to_text`` which in its simplest form
takes a list of list (or any sequence_ of sequences_) and format it as a table.
The data is assumed to be in `row-major order`_, meaning that the outer
sequence's elements are the rows of the table.

.. _row-major order: https://en.wikipedia.org/wiki/Row-major_order
.. _sequence:
.. _sequences: https://docs.python.org/2/glossary.html#term-sequence

.. code:: python

    >>> from tabletext import to_text
    >>> a = [["Code", "Name"],
             ["AD", "ANDORRA"],
             ["AE", "UNITED ARAB EMIRATES"],
             ["AF", "AFGHANISTAN"],
             ["AG", "ANTIGUA AND BARBUDA"]]
    >>> print to_text(a)

will output the following:

.. code::

    ┌──────┬──────────────────────┐
    │ Code │ Name                 │
    ├──────┼──────────────────────┤
    │ AD   │ ANDORRA              │
    ├──────┼──────────────────────┤
    │ AE   │ UNITED ARAB EMIRATES │
    ├──────┼──────────────────────┤
    │ AF   │ AFGHANISTAN          │
    ├──────┼──────────────────────┤
    │ AG   │ ANTIGUA AND BARBUDA  │
    └──────┴──────────────────────┘

You can customize the output with optional arguments:


.. code:: python

    >>> print to_text(a, header=True, corners="+", hor="-", ver="|",
                      header_corners="+", header_hor="=",
                      header_ver="!", formats=[">", "<"])

will output:

.. code::

    +======+======================+
    ! Code ! Name                 !
    +======+======================+
    |   AD | ANDORRA              |
    +------+----------------------+
    |   AE | UNITED ARAB EMIRATES |
    +------+----------------------+
    |   AF | AFGHANISTAN          |
    +------+----------------------+
    |   AG | ANTIGUA AND BARBUDA  |
    +------+----------------------+
    |   AI | ANGUILLA             |
    +------+----------------------+

See the Documentation_ section for more details about the optional arguments of
the ``to_text`` function.

Command line utility
~~~~~~~~~~~~~~~~~~~~

The command line utility reads from its input the table, each line representing
a row, its entries being separated by ``\t`` characters (configurable) and
outputs the formatted table to the standard output:

.. code:: bash

    $ df -h | tr -s ' ' \\t | cut -f1-6 | table --header
    ╒════════════╤══════╤══════╤═══════╤══════╤════════════════╕
    │ Filesystem │ Size │ Used │ Avail │ Use% │ Mounted        │
    ╞════════════╪══════╪══════╪═══════╪══════╪════════════════╡
    │ /dev/sda2  │ 25G  │ 14G  │ 9.5G  │ 60%  │ /              │
    ├────────────┼──────┼──────┼───────┼──────┼────────────────┤
    │ dev        │ 3.8G │ 0    │ 3.8G  │ 0%   │ /dev           │
    ├────────────┼──────┼──────┼───────┼──────┼────────────────┤
    │ run        │ 3.8G │ 756K │ 3.8G  │ 1%   │ /run           │
    ├────────────┼──────┼──────┼───────┼──────┼────────────────┤
    │ tmpfs      │ 3.8G │ 1.3M │ 3.8G  │ 1%   │ /dev/shm       │
    ├────────────┼──────┼──────┼───────┼──────┼────────────────┤
    │ tmpfs      │ 3.8G │ 0    │ 3.8G  │ 0%   │ /sys/fs/cgroup │
    ├────────────┼──────┼──────┼───────┼──────┼────────────────┤
    │ /dev/sda1  │ 511M │ 24M  │ 488M  │ 5%   │ /boot          │
    ├────────────┼──────┼──────┼───────┼──────┼────────────────┤
    │ tmpfs      │ 3.8G │ 372M │ 3.5G  │ 10%  │ /tmp           │
    ├────────────┼──────┼──────┼───────┼──────┼────────────────┤
    │ /dev/sda3  │ 15G  │ 9.8G │ 4.2G  │ 71%  │ /home          │
    ├────────────┼──────┼──────┼───────┼──────┼────────────────┤
    │ /dev/sda5  │ 77G  │ 46G  │ 27G   │ 64%  │ /media/data    │
    ├────────────┼──────┼──────┼───────┼──────┼────────────────┤
    │ tmpfs      │ 774M │ 16K  │ 774M  │ 1%   │ /run/user/1000 │
    └────────────┴──────┴──────┴───────┴──────┴────────────────┘

The available options can be printed with ``table --help`` and closely follow
the optional arguments of the library's ``to_text`` function as documented
here_.

.. _here: documentation_

Documentation
-------------

The optional arguments of the ``to_text`` function are as follows:

==================  ================  ================
Argument            Default           Description
==================  ================  ================
``formats``         ``None``          Format strings for the entries (see
                                      below)
``padding``         ``(1, 1)``        Left and right padding lengths
``corners``         ``"┌┬┐├┼┤└┴┘"``   Characters to use for the corners
``hor``             ``"─"``           Horizontal separation character
``ver``             ``"│"``           Vertical separation character
``header``          ``False``         Wether or not to display the first row
                                      as a header row
``header_corners``  ``"╒╤╕╞╪╡"``      Characters to use for the header row
                                      corners
``header_hor``      ``"═"``           Horizontal separation character for the
                                      header row

``header_ver``      ``"│"``           Vertical separation character for the
                                      header row
==================  ================  ================

More about some options:

* ``formats`` can be either a single format string, in which case it will be
  used for all entries, or a list of format strings, one per column of the
  table. The format strings must follow Python's `format specification`_. Note
  however that you don't have to specify the width since it is automatically
  computed. Useful format strings are ``"<"``, ``">"`` and ``"="`` for left
  align, right align and centered columns respectively.

* ``corners`` and ``header_corners`` are strings containing the corner
  characters to be used for rows and the header row respectively. Follow the
  same order as in the default values. Alternatively, you can specify only one
  character (that is, a string of length 1) which will be used for all corners.

.. _format specification: https://docs.python.org/2/library/string.html#format-specification-mini-language
