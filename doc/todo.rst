Stack (Hanging)
===============

* unify bus publishing

Todo
====

* exceptions (dbus.thermometer.Thermometer_Server.get_temperature)
* collapse history and thermometer into thermometer object which
  provides both interfaces
* plotly, graph pages

  * tooltips as links to thermometer pages for example
  * main area has one sub-template that divides main area in two,
    adding a div for "the graph", and a couple of alike possibities
    for further subclassing.
  * hierarchical naming through the area hierarchies created. for
    example <div id="path.to.element"></div>, and easier-to-check
    (make functions for them) references in css and graph placement.

* error managers

  * signal a HeatingError by subtype, pickle. oder gleich json, bissl
    unittesterei.
  * hook manager for specific errors in. w1 crap for example, need
    better reports, logging.
  * debug facilities for all

    * web/*, auch templates/
    * dbus/*
    * setup, on build/installation errors like ac_subst. logging
      there.

* Move dbus.ServerObject logic into dbus.lifecycle. Class decorator
  lifecycle.managed() or so, which simply ducktypes into obj.startup()
  and obj.shutdown() is class has the attribute. or so.

* Move thermometers_ini into config.thermometers_ini

* Update graphs: Json interface for history, plus calling JS in
  thermometer.html.

* DBus exceptions
  
  * simplify HeatingError to a minimum
    * create proxy classes (modify clients)
  * rename server-side objects to *_object
  * properly translate HeatingError (using .msg())

* thermometers.ini

  * detect duplicate thermometer names
  * error-tests
  * define exception(s)

* D-Bus

  * Where do D-Bus activation (.service) files go?
    https://stackoverflow.com/questions/31702465/how-to-define-a-d-bus-activated-systemd-service
  * How to generate the D-Bus config file from a template? (Paths like
    unix address and <servicedir> need to be substituted.)
