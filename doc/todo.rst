Stack (Hanging)
===============

* switches

  * openheating-switches.py

Todo
====

* controlling pumps. better name required. transport(from,
  to).{de,}activate() or something.

  * "beer spin off" below is a good generalization of pump control. a
    "pump" there is basically a heat on/off switch which can control
    pump switches or beer pot heaters (which are thermostats). so
    there need not be "pump" in that class.
  * hysteresis with on/off attributes

    * better say *upwards/downwards* instead for crossing the upper
      bound upwards and the lower bound downwards, resp.
    * simply tested, maybe start with that to heat up brain for this.

  * pump control logic

    * activate

      * activate hysteresis
      * start timer myself and thereby add a dependency? or should I
        add a poll() method whose call must be scheduled by the user?
        the former would ease usability, you just hook a parameterized
        pump dbus node (a nicely adapted pure python object) into the
        connection, and be done.

	best to add timer functionality into node, periodic only for
	now, start/stop (add this functionality into the node
	definition (in addition to the xml thing), to please security
	managers). after all, node is our heating-thing abstraction -
	propably rename it accordingly. maybe HeatingThing for
	now. does dbus and system (eventloop, timers) in the
	glib/gdbus way. for now. document it this way in the node
	docstring.

    * deactivate

      * switch off
      * stop timer

    * try out how @property works via dbus attributes, for status
      reads for example ("active" -> bool), or even better yet to
      control functionality. "active" as a read/write property.
    * on the dbus side, implement dbus properties in node. add dbus
      attribute support and provide an automatic mapping between those
      and natives.
    * must remain testable, although we need periodic state
      updates. timestamps everywhere.
    * the "timername"_*() interface from the HeatingThing definition.

      * start (into timer)
      * stop (into timer)
      * tick (from timer). reads new temperature, updates state, and
        does whatever needs to be done with state and switch updates.

    * nice opportunity for a new testcase helper, inject_timed()
      whatever.

* beer spin off
* home_faschingbauer web crap
* remove need for app.setup(), import in run(), makes no difference.
* error managers
* test setups

  * record temperatures in live system
  * replay in simulation, incl. fast forward

    * convert inexactly spaced timestamps into accurately spaced
      per-second timestamps (just because we have numpy arrays and
      scipy splice interpolation)
