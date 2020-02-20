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
............

This is a bit tedious (hope is that Raspbian's ``libgpiod`` package
will bring the Python binding in future versions). ``libgpiod``
requires the `autoconf archive
<https://www.gnu.org/software/autoconf-archive/>`_ which definitely
needs some love.

* *Install build dependencies*

  .. code-block:: shell

     (root)$ apt install autoconf
     (root)$ apt install libtool

* *Prepare for Build*

  .. danger:: *Rant!*

     I haven't found a way to set ``aclocal``'s M4 path into
     ``autoconf-archive/m4``, so I simply copy it to ``libgpiod/m4/``.

  .. code-block:: shell

     (jfasch)$ mkdir ~/hrmpf
     (jfasch)$ cd ~/hrmpf
     (jfasch)$ git clone git://git.sv.gnu.org/autoconf-archive.git
     (jfasch)$ git clone git://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git
     (jfasch)$ cp -r ~/hrmpf/autoconf-archive/m4 ~/hrmpf/libgpiod/m4

* *Build and Install*

  .. note::

     We install into ``/usr``. *Reason*: OpenHeating services are
     started by systemd, and there is no easy way to point its
     ``PYTHONPATH`` to somewhere else.

  .. code-block:: shell

     (jfasch)$ cd libgpiod
     (jfasch)$ autoreconf --force --install --verbose
     (jfasch)$ ./configure --prefix=/usr --enable-bindings-python
     (jfasch)$ make
     (root)$ make install

* *Fix bullshit*: ``gpiod`` module not found

  The previous step installed ``libgpiod``'s Python binding into
  ``/usr/lib/python3.5/site-packages/``. (The build system uses
  `Automake <https://www.gnu.org/software/automake/>`__ and its
  `Python support
  <https://www.gnu.org/software/automake/manual/html_node/Python.html>`__.)

  .. code-block:: shell

     $ ls -l /usr/lib/python3.5/site-packages/
     total 248
     -rw-r--r-- 1 root root 128878 Feb 19 13:59 gpiod.a
     -rwxr-xr-x 1 root root    986 Feb 19 13:59 gpiod.la
     -rwxr-xr-x 1 root root 117464 Feb 19 13:59 gpiod.so

  Reading `the documentation for Python's site module
  <https://docs.python.org/3.5/library/site.html>`__, Python should be
  able to pick it up from there. ``gpiod.so`` is the Python ``gpiod``
  module, a C extension in the form of a shared object.

  But no,

  .. code-block:: python

     >>> import sys
     >>> sys.version
     '3.5.3 (default, Sep 27 2018, 17:25:39) \n[GCC 6.3.0 20170516]'
     >>> import gpiod
     Traceback (most recent call last):
       File "<stdin>", line 1, in <module>
     ImportError: No module named 'gpiod'

  No ``site-packages`` in Python's module load path,

  .. code-block:: python

     >>> import sys
     >>> sys.path
     ['', '/usr/lib/python35.zip', '/usr/lib/python3.5', '/usr/lib/python3.5/plat-arm-linux-gnueabihf', '/usr/lib/python3.5/lib-dynload', '/usr/local/lib/python3.5/dist-packages', '/usr/lib/python3/dist-packages']

  .. danger::

     **WTF! It that an artifact of Debian/Raspbian?**

  Anyway ... knowing that we cannot simply fix that by adding
  ``/usr/lib/python3.5/site-packages`` to the environment (via
  ``/etc/profile.d/`` for example) because systemd does not pull that
  in (SysV init doesn't too btw.), we add it to
  ``/usr/lib/python3.5/sitecustomize.py``.

  .. code-block:: shell

     (root)$ cat <<EOF >> /usr/lib/python3.5/sitecustomize.py
     import site
     site.addsitedir('/usr/lib/python3.5/site-packages')
     EOF

  See if all is well,

  .. code-block:: shell

     $ python3
     Python 3.5.3 (default, Sep 27 2018, 17:25:39) 
     [GCC 6.3.0 20170516] on linux
     Type "help", "copyright", "credits" or "license" for more information.
     >>> import gpiod

Links
.....

* `libgpiod <https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/>`_
* `Kernel Doc <https://www.kernel.org/doc/Documentation/gpio/consumer.txt>`_
