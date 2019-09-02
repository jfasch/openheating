Dependencies
============

Install all software that is needed; see dependencies.rst

Installation
============

$ python setup.py install --prefix=/some/prefix

Create `openheating` user, ::

   # useradd --system openheating

Configure system DBus to allow us in, ::

   # cp /some/prefix/share/systemd/org.openheating.conf /etc/dbus-1/system.d/
   # systemctl reload dbus

Create and fill `/etc/openheating/`, ::

   # mkdir /etc/openheating
   # cp /some/prefix/share/installations/faschingbauer/thermometers.ini /etc/openheating/

Install systemd unit files, ::

   # cp /some/prefix/share/systemd/openheating-thermometer-service.service /etc/systemd/system

Enable and start services, ::

   # systemctl enable openheating-thermometer-service.service
   # systemctl start openheating-thermometer-service.service

