Dependencies
============

Install all software that is needed; see dependencies.rst

Installation
============

$ python3 setup.py install --prefix=/some/prefix

Create `openheating` user, ::

   # useradd --system openheating

Create and fill `/etc/openheating/`, ::

   # mkdir /etc/openheating
   # cp /some/prefix/share/installations/faschingbauer/thermometers.ini /etc/openheating/

Install systemd unit files, ::

   # cp /some/prefix/share/systemd/openheating-thermometer-service.service /etc/systemd/system

Install DBus service files (for bus activation). Location taken from
https://www.freedesktop.org/wiki/IntroductionToDBus/), except that its
neighbor directory ./system-services/ sounds more appropriate. ::

   # cp /some/prefix/dbus/org.openheating.ThermometerService.service /usr/share/dbus-1/system-services/

Configure system DBus to allow us in, ::

   # cp /some/prefix/share/systemd/org.openheating.conf /etc/dbus-1/system.d/
   # systemctl reload dbus

