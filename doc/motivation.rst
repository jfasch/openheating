Motivation
==========

Current Goal: Keep my House Warm
--------------------------------

First, a bit of history about heating here in my house.

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
