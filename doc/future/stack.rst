Stacks (Hanging)
================

These are my stacks (yes multiple, since I normally have multiple
tasks pending) that I maintain at high frequency. Each frame is one
work item that is currently being worked on. While I work on one item,
another one pops up (generally something that is needed for the
current one) and suspends the current item - forming a stack,
basically.

Hotwater Circuit Overtake
-------------------------

* toplevel main()-like thing

  done basically; the following pieces are missing.

  * watchdog. could for example periodically check thermometers in
    case everybody else forgets -> easy and funny, simply pull the
    line on error. should make sure that thermometers raises the
    currently active exception of each thermometer. add
    clear_exception() to Thermometer.
  * poll() on every participant in the game. could do toplevel error
    handling, using the exceptions of each poll call, being the only
    one that writes to .Errors. HAH! maybe best *be* the error logger.
  * error handling: carry a simple table of errors to handle with a
    watchdog pull.

* fix setup and installation

  * remove dbus activation
  * remove unit files except http
  * doc: move more of doc/ to toplevel: intro, installation,
    components, todo, panel

* generator: create necessary symlinks

Component Documentation
-----------------------

* Bloody "not implemented" pages

  * room refers to hysteresis
  * boiler likewise
