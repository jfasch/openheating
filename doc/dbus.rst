Python Bindings
===============

``pydbus``
----------

Looks promising, but I didn't get a custom bus to work. Only session
and service. Appears to be unmaintained.

``dbus-python``
---------------

Tried and tested with the initial attempt (``try-no1``), lets stick
with it.

Commandline Stuff
=================

Debug, Monitor
--------------

* d-feet

Calling
-------

::
    dbus-send --bus unix:path=$HOME/work/openheating/dbus/run/openheating-dbus-daemon.socket \
      --dest=org.openheating.ThermometerService \
      --type=method_call \
      --print-reply \
      /a/b \
      org.openheating.Thermometer.get_temperature

D-Bus Activation (failed)
=========================

Followed the "Activation" section in
https://www.freedesktop.org/wiki/IntroductionToDBus/.

Wrote a service file,
``org.openheating.ThermometerService.service``,::

  [D-BUS Service]
  Names=org.openheating.ThermometerService
  Exec=/home/jfasch/work/openheating/dbus/dbus-thermometer-service.py

Configured <servicedir> in the bus config file to point to the
directory containing the service file. dbus-daemon appeared to
recognize it, as it printed a message about "reloading" everytime I
modified the service file (or any file in that directory).

Upon calling, though, ::

  $ dbus-send --bus=unix:path=/home/jfasch/work/openheating/dbus/run/openheating-dbus-daemon.socket \
      --dest=org.openheating.ThermometerService \
      --type=method_call \
      --print-reply \
      /a/b \
      org.openheating.Thermometer.get_temperature
  Error org.freedesktop.DBus.Error.ServiceUnknown: The name org.openheating.ThermometerService was not provided by any .service files

``strace`` on the daemon revealed that it honored the activation
request somehow (it read the service file), but then decided to deny
the activation for whatever reason.
