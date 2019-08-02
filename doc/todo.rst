Stack (Hanging)
===============

* unify argparse composition
* properly choose session/system bus; unify

  * openheating.dbus.connection: add name=None parameter, and remove
    request_name()
  * openheating.dbus.connection: fallback=False

Thermometers
============

* thermometers.ini

  * implement other thermometer types than "fixed"
  * detect duplicate thermometer names
  * error-tests
  * define exception(s)

D-Bus
=====

* find out what dbussy.DBUS.NAME_FLAG_DO_NOT_QUEUE is
* Where do D-Bus activation (.service) files go?
* How to generate the D-Bus config file from a template? (Paths like
  unix address and <servicedir> need to be substituted.)
