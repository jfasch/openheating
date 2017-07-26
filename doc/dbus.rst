Debug, Monitor
==============

* d-feet

Calling
=======

dbus-send --bus unix:path=/var/run/openheating/openheating-dbus-daemon.socket \
  --dest=org.openheating.ThermometerService \
  --type=method_call \
  --print-reply \
  /a/b \
  org.openheating.Thermometer.get_temperature
