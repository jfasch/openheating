Cleanup
=======

* rm dbus/busconf/

Thermometers
============

* Thermometer service

  * Proper commandline parsing

    * configfile (thermometers.ini)
    * session/system bus

* client program: read temperatures from all thermometers

* thermometers.ini

  * implement other thermometer types than "fixed"
  * detect duplicate thermometer names
  * error-tests
  * define exception(s)

D-Bus Understanding
===================

* find out what dbussy.DBUS.NAME_FLAG_DO_NOT_QUEUE is
* bus.register(): fallback?
