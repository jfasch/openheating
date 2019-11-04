Stack (Hanging)
===============

* continue with home_faschingbauer web crap

Todo
====

* NodeDefinition

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

