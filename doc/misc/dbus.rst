D-Bus Things
============

Calling Object Methods
----------------------

Thermometer Service
...................

**ThermometerService.all_names**

::

  $ gdbus call --session \
       --dest org.openheating.ThermometerService \
	  --object-path / \
	  --method org.openheating.ThermometerService.all_names
  (['Oil', 'Wood'],)

**Thermometer.get_temperature**

::

  $ gdbus call --session \
       --dest org.openheating.ThermometerService \
	  --object-path /thermometers/Oil \
	  --method org.openheating.Thermometer.get_temperature
  (666.66600000000005,)

Introspection
-------------

List bus names (services)

::

  $ gdbus call --session \
      --dest org.freedesktop.DBus \
      --object-path /org/freedesktop/DBus \
      --method org.freedesktop.DBus.ListNames

Prettyprint object names provided by a service

::

   $ busctl --system tree org.openheating.ThermometerService

Debug, Monitor
--------------

::

   dbus-monitor --session 
