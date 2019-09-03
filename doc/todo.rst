Stack (Hanging)
===============

* openheating-http systemd unit, notify

Todo
====

* /etc/systemd/system seems like the wrong place to put unit files

* move from aiohttp to flask, jinja2 is directly usable there

* Thermometer refactoring

  * provide *abstract* access methods for
    openheating.Thermometer.{name,description}, and move those into
    subclasses
  * subclass a dbus proxy from openheating.Thermometer, caching the
    above attributes after first retrieval.
  * make this a pattern, eliminating the obscure ncessity to [0] index
    each dbus return

* DBus exceptions
  
  * simplify HeatingError to a minimum
    * create proxy classes (modify clients)
  * rename server-side objects to *_object
  * properly translate HeatingError (using .msg())

* Exceptions in asyncio
* thermometers.ini

  * implement other thermometer types than "fixed"
  * detect duplicate thermometer names
  * error-tests
  * define exception(s)

* D-Bus

  * find out what dbussy.DBUS.NAME_FLAG_DO_NOT_QUEUE is
  * Where do D-Bus activation (.service) files go?
    https://stackoverflow.com/questions/31702465/how-to-define-a-d-bus-activated-systemd-service
  * How to generate the D-Bus config file from a template? (Paths like
    unix address and <servicedir> need to be substituted.)
