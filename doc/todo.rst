Stack (Hanging)
===============

* Flask

  * add setup.py

Todo
====

* Use Flask.route() decorator on global app object which we keep in a
  wellknown place, say openheating.web.the_app.py.

  * Use url_for() as proposed. I don't know if current route
    establishment to App.__view_*() methods is expected. Factor
    __view's out into separate modules which then import
    openheating.web.the_app and use the Flask object from
    there. Better yet, do some __init__ trickery in openheating.web
    itself.

* Move dbus.ServerObject logic into dbus.lifecycle. Class decorator
  lifecycle.managed() or so, which simply ducktypes into obj.startup()
  and obj.shutdown() is class has the attribute. or so.

* Move thermometers_ini into config.thermometers_ini

* Update graphs: Json interface for history, plus calling JS in
  thermometer.html.

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
