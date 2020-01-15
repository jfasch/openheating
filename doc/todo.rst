Stack (Hanging)
===============

* hotwater circuit overtake

  * any commented-out tests in dbussuite_circuits?
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
  * poll() on every participant in the game. could do toplevel error
    handling, using the exceptions of each poll call, being the only
    one that writes to .Errors. HAH! maybe best *be* the error logger.
  * error handling: carry a simple table of errors to handle with a
    watchdog pull.

* plant runner service

  * add missing services

    * BoilerService
    * WoodOvenService
    * OilBurnerService
    * MixerService

  * Service.start()

    * replace find_exe with exe_dir or None (->search in path)
    * same with the config files. installed or from source, that's
      basically the question. should be consistent with the exes.
    * fix plant.pyconf

* see how we can write to temperature/switch files and force an update
  that is seen immediately

  * Thermometer.force_update(), maybe as a convenience function in
    PlantTestCase

    * instantiate client in PlantTestCase.start_plant())
    * move preliminary setup code from
      ThermometersSimulation.test__force_update_of_file_thermometer()
      to PlantTestCase
    * watch out for 'jjj'
    * eliminate Thermometer.inject_sample() in favor of force_update()
      from FileThermometer

  * re-enable other tests in ThermometersSimulation
  * PlantTestCase: provide timeline (eliminating all other occurrences
    of itertools.count)
  * move dbus/config.py to plant/

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

    * interface. hmm. we have toplevel code objects, programs made by
      primitives in in the program module, like everything else. why
      not just add another primitive program.lauch_code(), or simply
      recognize a coroutine ??? is there an api for that, I believe
      yes!!)

      then simply await the task by adding it to one of our running
      lists. hmm. wait(). child(). fire_off() or
      asyncio.create_task().

      add these as a replacement for launch(). look into "warning"
      type exceptions. how easy that could be.

  * next evolution step: marketing. on a group of buttons, pulse sine
    waves with varying frequencies.

    * forever(... hmmm .. something like ... with numpy.sine() on an
         itertools.cycle()d iterator.

	 on(red),
	 any(
	    # blink(... sine ... rate ... frequency -> iterator!!!)
	    # -> numpy blah await asyncio.sleep(...) so geil!
	    # -> presentation
	    # think about wait() child() whatever primitives.
	    call(pyprog, *args, **kwargs))
	    wait_button(red),
	 ),
	 any(
	    blink(red, 0.5),
	    wait_button(red)
	 ),
	 # annoy a bit more
	 any(
	    blink(red. 0.1),
	    wait_button(red),
	 ),
      )
	 
    * (**) @program() should work on range() too? that would be the
      hammer!
    * call(pycode) takes a code object (in whatever precompiled form),
      eval()s it (in whatever context, current?) and turns it into a
      program. hammer!

* populate conf/

  * move dbus/ and systemd/ into conf/
  * fix setup.py accordingly

* controlling pumps. better name required. transport(from,
  to).{de,}activate() or something.

  * "beer spin off" below is a good generalization of pump control. a
    "pump" there is basically a heat on/off switch which can control
    pump switches or beer pot heaters (which are thermostats). so
    there need not be "pump" in that class.
  * pump control logic

    * try out how @property works via dbus attributes, for status
      reads for example ("active" -> bool), or even better yet to
      control functionality. "active" as a read/write property.
    * on the dbus side, implement dbus properties in node. add dbus
      attribute support and provide an automatic mapping between those
      and natives.
    * must remain testable, although we need periodic state
      updates. timestamps everywhere.

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

* hardware woes. write that down when done (if ever), to bring a story
  in the GLT2020 talk.

  * internal gpios can only switch 50mA in total. controlling 16
    relays (via optocouplers; 2 LEDs and a ~500 resistor) is too
    hard. have to use transistors.

    story

    * learned the hard way that not all GPIOs have the same POR
      settings. from those visible on P1 header, GPIO0 through GPIO8
      are configured to have a pullup resistor (is it ~50K? check
      that), where the others have a pulldown resistor.

  * tried to use a mcp23017 IO expander via I2C. plan was to save tons
    of transistors and resistors, and simply connect it over I2C.

    that did not work out though. background: I use libgpiod (the new
    /dev/ interface) because all reserved GPIOs get properly reset to
    their original settings when the application terminates,
    auomatically.

    mcp23017 (respectively, drivers/pinctrl/pinctrl-mcp23s08.c) does
    not do that. must be a bug which sure can be fixed. I'd really
    like to know the gpiod implementation, but not now :-)

    BCM GPIOs (LED on GPIO26, for 3 seconds): ::

      $ gpioset -m time -s 3 pinctrl-bcm2835 26=1

    MCP23017 GPIOs (LED on GPA0, forever): ::

      $ gpioset -m time -s 3 mcp23017 0=1

  * buy one of those I2C/W1 masters and do all that in
    hardware. bit-banging is no good, I see errors from time to time
    (worse yet, reading temperatures of 0 degrees, unusable).

    even more so, I am running out of GPIOs. according to
    https://www.raspberrypi.org/documentation/configuration/device-tree.md#part4.6,
    UART0 takes the pins of GPIO 14,15, so I configured it away. 15
    still does not work though.
