Cleanup
=======

* rm dbus/busconf/

Thermometers
============

* thermometers.ini

  * implement other thermometer types than "fixed"
  * detect duplicate thermometer names
  * error-tests
  * define exception(s)

* Thermometer service

  * Proper commandline parsing

    * configfile (thermometers.ini)
    * session/system bus

D-Bus Understanding
===================

* find out what dbussy.DBUS.NAME_FLAG_DO_NOT_QUEUE is
* bus.register(): fallback?
