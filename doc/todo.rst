Stack (Hanging)
===============

* error management

  * test for dbus node, starting thermometers and errors
  * proper match rules for signal
  * dbusutil: convenience get_object_iface(), to be used in all client
    wrappers. see ThermometerCenter_Client.__get_object_iface().

    * signal definition, offered by the dbus objects.
    
      this is the normal use case. the dbus spec goes out of the way of
      defining such a relationship: signals pop directly out of the dbus
      connection, and this is where user code picks them up.
    
    * decorator that participates an "object" in siganl
      reception. maintains a list (globally unfortunately; could wrap all
      that - signal filters, loop, whatelse? - in a dbus_context class
      maybe) that maps signal parameters onto callables.
    
    * tests. all via openheating-errors.py level tests is a bit hard.
    
      * signal filters have nothing to do with dbus objects. just a mixin
        between dbus and me. a mapping that is used there, indidentally
        mapping dbus names blah onto something else. gets filled and used.
      * decorator tests.
      * and finally, errors. should i start to decouple dbus from logic
        now? yes!

* print stderr of service processes when test has failed

  * remove context manager hooks from Controller
  * remove services ctor parameter from Controller

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

* Move thermometers_ini into config.thermometers_ini

* Update graphs: Json interface for history, plus calling JS in
  thermometer.html.

* thermometers.ini

  * detect duplicate thermometer names
  * error-tests
  * define exception(s)

