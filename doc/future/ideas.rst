Lots of Vague Ideas
===================

An unordered list of not-so-vague ideas; to be done in the near
future.

* json interface, without any protocol, simply modeled on top of whats
  needed:

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

Project Structure Cleanup
-------------------------

* populate conf/

  * move dbus/ and systemd/ into conf/
  * fix setup.py accordingly

Documentation
-------------

Hardware Woes
- - - - - - -

Write that down when done (if ever), to bring a story in the GLT2020
talk.

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

More Heatingisms
----------------

* PID controller

  * example here: http://cgkit.sourceforge.net/doc2/pidcontroller.html#PIDController
  * explanation: http://en.wikipedia.org/wiki/PID_controller

* Curve to adjust radiator temperature based on outside temperature

  * Heizkurve (german):
    http://www.heizungsfinder.de/heizung/heizkurve-einstellen
