.. contents:: Table of Contents

Installation Notes
==================

Dependencies
------------

DBus: pydbus
............

::

   # pip3 install --system pydbus

systemd
.......

(At least) openheating-http.py uses it to notify systemd that it is
has finished startup and is running. (The service is Type=notify, and
not Type=dbus as most others.)

::

   # apt install python3-systemd

Flask
.....

::

   # pip3 install --system flask

GPIO: libgpiod
..............

``libgpiod`` is a C library directly on top of the descriptor based
GPIO interface.

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
++++++++++++

This is a bit tedious (hope is that Raspbian's ``libgpiod`` will bring
the Python binding in future versions). ``libgpiod`` requires the
`autoconf archive <https://www.gnu.org/software/autoconf-archive/>`_
which definitely needs some love.

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
+++++

* `libgpiod <https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/>`_
* `Kernel Doc <https://www.kernel.org/doc/Documentation/gpio/consumer.txt>`_


Installation
------------

$ python3 setup.py install --prefix=/some/prefix

Create `openheating` user, ::

   # useradd --system openheating

Create and fill `/etc/openheating/`, ::

   # mkdir /etc/openheating
   # cp /some/prefix/share/installations/faschingbauer/thermometers.pyconf /etc/openheating/

Install systemd unit files, ::

   # cp /some/prefix/share/systemd/openheating-*.service /etc/systemd/system

Configure system DBus to allow us in, ::

   # cp /some/prefix/share/dbus/org.openheating.conf /etc/dbus-1/system.d/
   # systemctl reload dbus

Start necessary services, ::

   # systemctl enable openheating-errors.service
   # systemctl enable openheating-thermometers.service
   # systemctl enable openheating-http.service

   # systemctl start openheating-errors.service
   # systemctl start openheating-thermometers.service
   # systemctl start openheating-http.service
