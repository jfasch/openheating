Heating Control System
======================

Will once solve my needs for a heating control system that comprehends
a historically grown constellation.

* Two heat sources
  * Oil (fully automatic)
  * Wood (manual firing, in the living room). Wood currently dominates oil in a brutal way, in that a bi-metal temperature switch disbles oil burning abruptly when wood is coming.
* Two heat sinks
  * Water; a 1000l buffer, where potable water is exchanged through
  * Radiators across the house, in a single circuit

There is a third possible heat source: a solar panel, producing hot
water when sun is on. Heats up the water buffer in a separate circuit,
controlled by a separate unit (which works and need not be replaced).

There is a circuit which can take heat from hot water. When there is
sun there is hot water. If the house needs heating (nights are still
cold), this could be done. Currently it cannot.

Rant
----

When I take a step back and look at the workarounds in our heating
system, I can see that software is harder than hardware. It is common
knowledge among plumbers how to install a wood oven alongside an oil
burner, without touching the existing heating control.

Since I started to think about this project, I have seen many house
heatings built around a software that cannot be modified. This
aberration - software harder than hardware - is not specific to house
heating systems, as it seems. This little project is my contribution
to revert that aberration.

Wish List
---------

While the main impetus for this project is to bring my own system to
its intended functionality, a definitive intent is to keep things
apart as far as possible. For example, I have a wood/oil combination
of heat sources. Software contains separate classes for each, combined
by a dedicated third class.

This is a higher level wish list, by decreasing priority. Details are
found in the issue tracker.

* Coordinate heat sources and sinks in an intelligent automatic way
  * When wood heat is coming, oil should be faded out gently (there's plenty of time).
  * A switching valve is currently turned manually; this is due to that "heating control" we currently have. (Was about €300, gosh)
* Bring the spare hot water in house heating. Not prio-1 right now, but will come.
* Control solar water. Works as-is, so low prio. Can be done when all else is mature; will be trivial then.
  * Thought: integrate with water buffer's mechanism. He needs heat when there's no sun, during night for example. Could read weather forecast and defer his need.
* This list can be extended to no end

Inner Beauty
------------

* Written in Python3
* Distributed using DBus, to provide
  * Sensors over Ethernet/TCP (I distribute them across the house, using Raspies)
  * Displays
  * Remote controls
  * Configuration using dconf (way in the future though)
  * (whatever)
