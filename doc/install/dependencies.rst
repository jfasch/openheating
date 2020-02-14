Dependencies
============

DBus: pydbus
------------

We distribute components over `DBus <http://dbus.freedesktop.org/>`__,
using `pydbus <https://github.com/LEW21/pydbus>`__.

::

   # pip3 install --system pydbus

`systemd` Startup Notification
------------------------------

(At least) `openheating-http.py` uses it to notify `systemd` that it
has finished startup and is running. (The HTTP service is
`Type=notify`, and not `Type=dbus` as the others.)

::

   # apt install python3-systemd

Flask
-----

Web is done using `Flask
<https://www.palletsprojects.com/p/flask/>`__. Simple and easy.

::

   # pip3 install --system flask

Gradients, Interpolation, Graphs
--------------------------------

Web has fancy temperature charts, and I believe there's a spline
interpolation done somewhere.

:: 

   # pip3 install --system numpy scipy matplotlib
   # pip3 install --upgrade --system numpy scipy matplotlib

(Upgrading makes sense, especially with these)

GPIO: `libgpiod`
----------------

`libgpiod` is a C library directly on top of the descriptor based GPIO
interface.

The "integer based" sysfs interface has been deprecated a while ago
(Linux 4.8). It would be sufficient for our purposes - plain set/get
-, but it is on the way out.

`libgpiod
<https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/>`_ has a
Python binding, but unfortunately there is no Raspbian package as of
2019-07-29 that has it. (There is `gpio-next
<https://pypi.org/project/gpio-next/>`_ on PyPI, but it is maintained
independently from libgpiod.)

Installation
- - - - - - 

This is a bit tedious (hope is that Raspbian's ``libgpiod`` package
will bring the Python binding in future versions). ``libgpiod``
requires the `autoconf archive
<https://www.gnu.org/software/autoconf-archive/>`_ which definitely
needs some love.

Check build dependencies::

   # apt install autoconf
   # apt install libtool

Build and install::

   $ mkdir ~/hrmpf
   $ cd ~/hrmpf
   $ git clone git://git.sv.gnu.org/autoconf-archive.git
   $ git clone git://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git
   $ cp -r ~/hrmpf/autoconf-archive/m4 ~/hrmpf/libgpiod/m4  # see rant below
   $ cd libgpiod
   $ autoreconf --force --install --verbose
   $ ./configure --prefix=/usr/local --enable-bindings-python
   $ make
   $ sudo make install

*Rant*: I haven't found a way to set ``aclocal``'s M4 path into
``autoconf-archive/m4``, so I simply copy it to ``libgpiod/m4/``.

Set paths (take the ``PYTHONPATH`` value from the messages of the
``libgpiod`` build, as it depends on the Python version you are using)::

   $ export PYTHONPATH=/usr/local/lib/python3.5/site-packages:$PYTHONPATH
   $ export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

Better yet, create ``/etc/profile.d/openheating.sh``::

   export PYTHONPATH=/usr/local/lib/python3.5/site-packages:$PYTHONPATH
   export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

See if all is well,::

   $ python3
   Python 3.5.3 (default, Sep 27 2018, 17:25:39) 
   [GCC 6.3.0 20170516] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import gpiod

Links
- - -

* `libgpiod <https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/>`_
* `Kernel Doc <https://www.kernel.org/doc/Documentation/gpio/consumer.txt>`_