Stack (Hanging)
===============

* Temperature history

  * "reduced" history, covering a day or so; mainly for display. as
    opposed to the short-term history where we base decisions on.

* Flask

  * add setup.py

Todo
====

* Use Flask.route() decorator on thread-specific app object which we
  keep in a wellknown place, say openheating.web.the_app.py.

  * Use url_for() as proposed. I don't know if current route
    establishment to App.__view_*() methods is expected. Factor
    __view's out into separate modules which then import
    openheating.web.the_app and use the Flask object from
    there. Better yet, do some __init__ trickery in openheating.web
    itself.

  * Thread specific (there is a threading decorator for it)

* Move dbus.ServerObject logic into dbus.lifecycle. Class decorator
  lifecycle.managed() or so, which simply ducktypes into obj.startup()
  and obj.shutdown() is class has the attribute. or so.

* logging

  * dbus.Thermometer.{startup,shutdown} (debug)

* /etc/systemd/system seems like the wrong place to put unit files
* DBus exceptions
  
  * simplify HeatingError to a minimum
    * create proxy classes (modify clients)
  * rename server-side objects to *_object
  * properly translate HeatingError (using .msg())

* Exceptions in asyncio
* thermometers.ini

  * detect duplicate thermometer names
  * error-tests
  * define exception(s)

* D-Bus

  * find out what dbussy.DBUS.NAME_FLAG_DO_NOT_QUEUE is
  * Where do D-Bus activation (.service) files go?
    https://stackoverflow.com/questions/31702465/how-to-define-a-d-bus-activated-systemd-service
  * How to generate the D-Bus config file from a template? (Paths like
    unix address and <servicedir> need to be substituted.)
