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
