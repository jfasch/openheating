Pointless Blinking and Switching with Python, libgpiod, and asyncio
===================================================================

CV
--

 * Master in Mathematics/Informatics from TU Graz
 * Long years employed as programmer, architect etc. with different
   companies in and near Graz
 * Self employed since 2008, doing projects and trainings around Linux
 * See my [homepage](http://www.faschingbauer.co.at/) for more

Abstract
--------

It's not that GPIO is a new topic in Linux and Python - everybody does
it. This talk - live hacking, mostly - takes the opportunity to bring
up a few questions (and try to answer them):

 * Which GPIO interface should I use?
 * Why isn't multithreading the best answer to concurrency, generally?
 * How can decorators be used to enable a functional programming
   style, and to increase job security?

Topics
------

No matter what the use case, there are a couple of things that I want
to show.

 * The [new GPIO userspace interface of the
   kernel](https://lwn.net/Articles/565662/), and an accompanying
   userspace library, [libgpiod](https://github.com/brgl/libgpiod).
    * Why is complicated better than simple?
    * Why is sysfs GPIO deprecated?
    * What's wrong with RPi.GPIO?
 * [Python
   asyncio](https://docs.python.org/3/library/asyncio.html). GPIO
   interrupts are regular file descriptor based events, and it makes
   sense to integrate those with asyncio. 
    * Why is multithreading generally _not_ the best answer to
      concurrency?
    * What is an event loop?
    * What's the role of asyncio?
 * Functional programming style. For easy configuration of LED and
   button logic, and for fun, we will see what functional programming
   can do for you and how this is achieved. (Hint: decorators)

Use Case
--------

This talk is a about a spin-off of my long term [OpenHeating
project](https://github.com/jfasch/openheating) which will never be
done. It's easier with a spin-off - _a retro style control panel_.

Nowadays control panels of, say, heating control systems consist of a
monitor with a touch screen, a lot of fancy (web) programming, and
nothing else. **Boring**.

Imagine a retro style control panel. This would consist of a bunch of
LEDs and switches (most of the switches will have their own LEDs built
in). The LEDs would visualize the state of the heating system, such as
...

* pump on/off
* burner producing heat
* warm water boiler temperature below threshold

The switches would be used to control certain aspects of the system,
such as ...

* activating the warm water circuit
* disabling the oil burner
* acking error conditions that have been resolved

Each LED has different blinking patterns; for example, the LED that
visualizes the state of the boiler,

* If the boiler does not contain enough hot water, the LED will blink
  at a fast rate, "demanding".
* If the water is being produced, it will blink at a slower rate,
  "coming".
* If all is well, it will be off.

As you can imagine, there are quite a few of these patterns around
(there's the error LED blinking the "SOS" Morse sequence) that need to
be managed. They have to be put intp place when MQTT messages come in,
canceled and overwritten by different patterns, and so on.
