Stack (Hanging)
===============

* hotwater cycle overtake

  * openheating-circuits.py
  
    * pyconf
    * can we abstract *_Center? CircuitCenter would be the third.
    * http: menu for circuits
    * tests
  
      * poll_until(predicate, timeout)

    * toplevel main()-like thing. 

      * watchdog. could for example periodically check thermometers in
	case everybody else forgets -> easy and funny, simply pull the
	line on error. should make sure that thermometers raises the
	currently active exception of each thermometer. add
	clear_exception() to Thermometer.
      * poll() on every participant in the game. could do toplevel
	error handling, using the exceptions of each poll call, being
	the only one that writes to .Errors. HAH! maybe best *be* the
	error logger.
      * error handling: carry a simple table of errors to handle with
	a watchdog pull.
  
Todo
====

* blink

  * context, maybe added as a closure in @program(). geil -> add to
    presentation.
  * tests
    1. count down until value on each run. program name sub(), subs an
       object contained in a closure. together with a check, maybe
       cmp(sub(100),0).
    1. while loop, as a logical extension.
  * next evolution step: add python code and asyncio logic. pieces
    needed.

    * read up on globals() and locals(), and lookup in general
    * python code that is run in every lauch(), taking context (global
      variables? or something that can mimic this? is there a way to
      run a coroutine with a specialized context? easily? lets own the
      dot in ... wtf ... maybe something extensible in collections?
    * task management. is there something built in to
      asyncio. routines that are available to programs.

      * asyncio.ensure_future(), have to take care of yourself. likely
	catching CancelledError and maybe do cleanup.
      * program.child(). automatic cleanup on cancel().
      * program.wait(). await launch(). geil.

* populate conf/

  * move dbus/ and systemd/ into conf/
  * fix setup.py accordingly

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


* panel

  * play queue button, evtl. mit reset

    * task/coro started off doing a wait on a asyncio.Queue
    * maintains a task that it cancels/restarts appropriately as
      requests come in
    * requests are short programs that operate on the
      led/button/ledbutton combination

  * json interface, without any protocol, simply modeled on top of
    whats needed:

    * receive notification -> subscribe.

      * errors
      * state change monitors (emitting events) in every node. 

	* for example oil on off, wood request firing, oil
          disabled/enabled
	* class State with set/get. maybe some metaprogramming, owning
          the dot.

    * sending notification -> publish.

      * requests to for example, disable oil, ack wood firing
        requested state, ...

    * maybe on top of that, a synchronous call with a timeout. request
      cookie in the response? crap, ask google for solutions.

  * mqtt. payload decoded as json, topics encoded as dbus object
    names.

    * maybe pull defined names out of dbus, into a common "naming"
      module. use it from

      * dbus. generate dbus names and paths from there.
      * mqtt. generate topics and json messages from there.

      Could even pull interface_repo out of dbus, generating XML from
      an independent representation (easily done with namedtuple which
      is named for typed access, and iterable for a generator).

    * alternatives

      * http. status polling? no way.

* beer spin off
* error managers
* test setups

  * record temperatures in live system
  * replay in simulation, incl. fast forward

    * convert inexactly spaced timestamps into accurately spaced
      per-second timestamps (just because we have numpy arrays and
      scipy splice interpolation)
