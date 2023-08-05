
pysamloader-gui
===============

``pysamloader-gui`` is a kivy based GUI frontend to the ``pysamloader`` python
library for writing flash on Atmel's ARM chips via SAM-BA.

See the ``pysamloader`` documentation at
`ReadTheDocs <http://pysamloader.readthedocs.org/en/latest/index.html>`_. for
information about device support and features. This GUI is intended to be
simple, straightforward, and opinionated. It does not expose a great deal of
flexibility, and is intended to 'just work'.


Requirements & Installation
---------------------------

``pysamloader-gui`` should work on any platform which supports ``python`` and
``kivy``. It is best tested on Linux followed by on Windows (10 and 7).

In general, ``pysamloader-gui`` is expected to be pip-installed. It can be safely
installed into a virtualenv. As long as you have a functioning python 
installation of sufficient version, installing ``pysamloader-gui`` would be simply :

.. code-block:: console

    $ pip install pysamloader-gui

If you require pre-built binaries, they are available for 64-bit Linux and 
Windows. However, be aware that these binaries are not thoroughly tested, 
and your mileage may vary based on your specific operating system and machine 
architecture. You will also have to manually copy the included ``devices`` 
folder to the correct location.

When using binary packages, the included ``devices`` folder contains the
included device support modules, each of which is a python file with a
single class of the same name, containing device specific information about
one device. This folder should be copied into a separate location where you can
safely add, remove, or modify device configuration as needed. This device
library is shared with the ``pysamloader`` CLI application, which need not be
separately installed in order to the the GUI application. The location is
that provided by ``user_config_dir`` of the python ``appdirs`` package
for the ``pysamloader`` application, specifically :

    - Linux : ``~/.config/pysamloader``
    - Windows : ``C:\Users\<username>\AppData\Roaming\Quazar Technologies\pysamloader``

(Also see the ``pysamloader`` documentation).

The current ``pysamloader-gui`` windows .msi installer will create this folder
and populate it as a part of the install process.

If you wish to develop, modify the sources, or otherwise get the latest 
version, it can be installed from a clone of the git repository (or from a 
source package) as follows :

.. code-block:: console

    $ git clone https://github.com/chintal/pysamloader-gui.git
    $ cd pysamloader
    $ pip install -e .


Links & Other Information
-------------------------

Links
.....

The latest version of the sources can be found at
`GitHub <https://github.com/chintal/pysamloader-gui>`_. Please use GitHub's features
to report bugs, request features, or submit pull/merge requests.

``pysamloader-gui`` is distributed under the terms of the
`GPLv3 license <https://www.gnu.org/licenses/gpl-3.0-standalone.html>`_ .
A copy of the text of the license is included along with the sources.

I can be reached directly by email at shashank at chintal dot in.
