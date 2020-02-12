OpenHeating: Open Source Heating Control System
===============================================

.. toctree::
   :hidden:
   :maxdepth: -1

   doc/install/index
   doc/index.rst
   doc/future/index
   doc/marketing/index

An open source heating system that is being developed to solve my
particular needs,

* Be able to have two *alternative heat sources*, *Oil* and *Wood*.
* *Switch between them automatically*; for example when somebody
  lights the wood stove, the oil burner must be taken down gracefully
  (heat it up to its limit one last time, and reap the hot water).
* *Configuration* ("I want the heat to start coming at four in the
  morning so it's comfy at six when I get up") need not be better than
  in the current off-the-shelf system. It cannot not be done worse, so
  the first shot will be a config file that is edited with emacs. It
  will be a web interface eventually though, undoubtedly.

OpenHeating will once achieve world domination through its flexible
design. It will be open enough to nondestructively add such things as

* Using an "Algorithm" (for the technically inclined: this is "machine
  learning") to take the weatherforecast into account for example.
* Send out email (does anybody still use SMS?) on errors.
* Post big data into the cloud. Not that I'm a fan of it, but others
  sure are.

Current Goal: Keep my House Warm
--------------------------------

But lets not push too hard, but rather start with the basics. First, a
bit of history about heating here in my house.

Initially, somewhere around 25 years ago when the (one-family) house
was built (near Graz/Austria), there was only one way to heat:
**OIL**. The situation has changed slightly, there are many
alternatives like ground heat. Those are not exactly cheap, and oil
companies are still permitted to give financial incentives to the
undetermined.

A few years ago, I decided to establish a second heat source: a wood
stove in the living room. In addition to its nice looks, it can feed
heating water into the system, in parallel to the oil heating. The
stove is used as often as possible (I work from home as much as I
can), and only when there's nobody at home the oil is on.

So far so good. Should be easy to control.

* Two heat sources

  * Oil (fully automatic)
  * Wood (manual firing, in the living room). Wood currently dominates
    oil in a brutal way, in that a bi-metal temperature switch disbles
    oil burning abruptly when wood is coming.

* Two heat sinks

  * Water; a 1000l buffer, where potable water is exchanged through
  * Radiators across the house, in a single circuit

Rant
----

*But no:* When I take a step back and look at the workarounds in our
heating system, I can see that software is harder than hardware. It is
common knowledge among plumbers how to install a wood oven alongside
an oil burner, without touching the existing heating control.

Since I started to think about this project, I have seen many house
heatings built around a software that cannot be modified. This
aberration - software harder than hardware - is not specific to house
heating systems, as it seems. This little project is my contribution
to revert that aberration.

Plan
----

While the main impetus for this project is to bring my own system to
its intended functionality, a definitive intent is to keep things
apart as far as possible. Components on the horizon (or even yet in
place; I do not update written material regularly):

* Sensors all over the place, fancy histograms on a web page (done).
* Switch pumps on and off, based upon temperatures in the heat source
  and heat sink.
* A combined heat source which *contains* oil and wood (yay
  overengineering), and acts as one single heat source to the rest of
  the system.
* Inside that combined heat source, one mixer valve that adjusts its
  position according to the respective temperatures of oil and wood.
* Ah yes, error management (in fact, I started with that) (partly
  done).
* Did I forget something?

Inner Beauty
------------

* Written in Python
* Components loosely coupled in D-Bus
* Components managed with systemd
* GPIOs controlled not using the `sysfs interface
  <https://www.kernel.org/doc/Documentation/gpio/sysfs.txt>`__ (which
  is deprecated), but rather with the newer `gpiod
  <https://github.com/brgl/libgpiod/blob/master/README>`__.
* Web done with `flask <https://palletsprojects.com/p/flask/>`__.

Documentation
-------------

The state of documentation is a drama. Ok, the thing is in the works,
but documentation will always be a drama. All of the existing
documentation is found in :doc:`doc/index`.

* For my own purposes, I maintain an `installation document
  <doc/install.rst>`__.
* Same with the `todo list <doc/todo.rst>`__.
