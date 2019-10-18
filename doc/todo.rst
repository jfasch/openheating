Stack (Hanging)
===============

* unify bus publishing

  * dbusutil.run_server(): watch signals (calling callable)
  * dbus: add check if busname is already had, and fail accordingly
    (we do not start a temporary bus in the fixture, but attach to the
    session bus - which cries for such situations)
  
    (RuntimeError is raised in such a case btw)
  * remove dbusutil.publish()
  * lifecycle thermometer service: thread shutdown
  * encapsulate main loop singleton once and for all, and document the
    mess there.
  * test service wrappers: remove suppress_stderr. instead, capture
    stderr and output that on test failure.

Todo
====

* NodeDefinition

  * hehe: class decorator which makes a class into a dbus node. could
    be done now. -> dbus.util.nodedef()
  * parse XML, and check for presence of methods and signals. 

    * This way errors appear at class composition time, rather than
      late during bus publishing.
    * Even more so, we could additionall wrap every such method in its
      @unify_error decorator *automatically*. Cool!

* split dbusutil into consts.py containing the IDL stuff, for
  example. cmdline.py for blah. node.py for
  NodeDefinition. exception.py for all the exception conversion.

  * done with the exception conversion stuff, pull pydbus error
    mapping into that same location (possibly only *using* it from
    dbus.__init__).

    Write a big fat docstring which says how HeatingError instances
    make it across the bus.

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

<<<<<<< HEAD
  * find out what dbussy.DBUS.NAME_FLAG_DO_NOT_QUEUE is
=======
  * Where do D-Bus activation (.service) files go?
    https://stackoverflow.com/questions/31702465/how-to-define-a-d-bus-activated-systemd-service
>>>>>>> d8661d0971cffc435129f0cf6b3b7c874924f635
  * How to generate the D-Bus config file from a template? (Paths like
    unix address and <servicedir> need to be substituted.)
