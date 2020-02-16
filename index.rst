OpenHeating: Open Source Heating Control System
===============================================

.. toctree::
   :hidden:
   :maxdepth: -1

   doc/install/index
   doc/motivation
   doc/future/index
   doc/faschingbauer/index.rst
   doc/marketing/index
   doc/misc/index.rst

Why Yet Another Heating System?
-------------------------------

Off the shelf heating control unit are rather limited.

* Configuration is rather lame in all cases. Heating control's
  paradigm has always been "16 bit microcontroller and 7-segment
  displays" as it seems.
* Cannot control an arbitrary number of heating circuits. Chances are
  that you have to buy a new (and more expensive) control unit when
  you decide to add one more circuit to the system.
* Cannot coordinate multiple heat sources. For example, here in `my
  <http://www.faschingbauer.co.at/>`__ house there is an old and dirty
  oil firing, and a newer wood stove in the living room. No way with
  any affordable control unit.

OpenHeating addresses all these limitations, especially the "multiple
heat sources" limitations. It runs on Linux (my installation is a
`Raspberry <https://www.raspberrypi.org/>`__), so yes there is
internet and many possibilities.

This is a diagram of the situation in my house; click on the symbols
to get to the software components behind them. Don't be upset if a
link you click points to a placeholder page - I'm working on it :-)

.. raw:: html

    <svg xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 250 200">

      <defs>
	<g id="pump">
	  <circle
	      cx="10" cy="10" r="10"
	      style="fill:rgb(255,255,255);stroke-width:0.5;stroke:rgb(0,0,0)"/>
	  <polyline
	      points="20,10 4,18 4,2"
	      style="fill:rgb(0,0,0)"/>
	  />
	</g>
	<g id="mixer">
	  <polyline
	      points="0,5 0,15 10,10 0,5"
	      style="fill:rgb(255,255,255);stroke-width:0.5;stroke:rgb(0,0,0)"/>
	  <polyline
	      points="20,5 20,15 10,10 20,5"
	      style="fill:rgb(255,255,255);stroke-width:0.5;stroke:rgb(0,0,0)"/>
	  <polyline
	      points="5,0 15,0 10,10 5,0"
	      style="fill:rgb(255,255,255);stroke-width:0.5;stroke:rgb(0,0,0)"/>
	</g>
      </defs>

      <image
	  id="holzofen"
	  xlink:href="_static/heating-diagram/holzofen.png" 
	  x="0" y="0"
	  width="50" height="50" />

      <image
	  id="oelbrenner"
	  xlink:href="_static/heating-diagram/oelbrenner.png" 
	  x="0" y="130"
	  width="50" height="70"
	  style="fill:none;stroke-width:0.5;stroke:rgb(0,0,0)"/>

      <image
	  id="radiatoren"
	  xlink:href="_static/heating-diagram/radiator.png" 
	  x="200" y="0"
	  width="50" height="50" />

      <image
	  id="boiler"
	  xlink:href="_static/heating-diagram/boiler.png" 
	  x="200" y="120" 
	  width="50" height="80" />

      <use
	  id="mischer-holz-oel"
	  xlink:href="#mixer" 
	  x="80" y="160" />

      <!-- VORLAUF OELBRENNER -->
      <line 
	  id="vl-oelbrenner"
	  x1="50" y1="170" x2="80" y2="170"
	  style="stroke-width:2;stroke:rgb(255,0,0)"/>
      <!-- VORLAUF HOLZOFEN -->
      <polyline 
	  id="vl-holzofen"
	  points="50,20 90,20 90,160"
	  style="fill:none;stroke-width:2;stroke:rgb(255,0,0)"/>

      <!-- RUECKLAUF HOLZOFEN -->
      <line 
	  id="rl-holzofen-1"
	  x1="70" y1="183" x2="70" y2="150"
	  style="fill:none;stroke-width:2;stroke:rgb(0,0,255)"/>
      <line 
	  id="rl-vl-holzofen"
	  x1="80" y1="140" x2="90" y2="140"
	  style="fill:none;stroke-width:2;stroke:rgb(255,0,0)"/>
      <use
	  id="mischer-holz"
	  xlink:href="#mixer" 
	  transform="rotate(90,70,140)"
	  x="60" y="130" />
      <line 
	  id="rl-holzofen-2"
	  x1="70" y1="110" x2="70" y2="130"
	  style="fill:none;stroke-width:2;stroke:rgb(0,0,255)"/>

      <use
	  id="pumpe-holzofen" 
	  xlink:href="#pump" 
	  transform="rotate(-90,70,100)"
	  x="60" y="90" />
      
      <polyline 
	  id="rl-holzofen-2"
	  points="70,90 70,30 50,30"
	  style="fill:none;stroke-width:2;stroke:rgb(0,0,255)"/>

      <!-- VORLAUF WARMWASSER -->
      <line
	  id="vl-warmwasser-1"
	  x1="100" y1="170" x2="160" y2="170"
	  style="stroke-width:2;stroke:rgb(255,0,0)"/>
      <use
	  id="pumpe-warmwasser"
	  xlink:href="#pump" 
	  x="160" y="160" />
      <line
	  id="vl-warmwasser-2"
	  x1="180" y1="170" x2="200" y2="170"
	  style="stroke-width:2;stroke:rgb(255,0,0)"/>

      <!-- VORLAUF HEIZKREIS -->
      <line
	  id="vl-heizkreis-1"
	  x1="140" y1="170" x2="140" y2="150"
	  style="stroke-width:2;stroke:rgb(255,0,0)"/>
      <use
	  id="mischer-heizkreis"
	  xlink:href="#mixer" 
	  transform="rotate(-90,140,140)"
	  x="130" y="130" />
      <line
	  id="vl-heizkreis-2"
	  x1="140" y1="130" x2="140" y2="110"
	  style="stroke-width:2;stroke:rgb(255,0,0)"/>
      <use 
	  id="pumpe-heizkreis"
	  xlink:href="#pump" 
	  transform="rotate(-90,140,100)"
	  x="130" y="90" />
      <polyline
	  id="vl-heizkreis-3"
	  points="140,90 140,20 200,20"
	  style="fill:none;stroke-width:2;stroke:rgb(255,0,0)"/>

      <!-- RUECKLAUF HEIZKREIS -->
      <polyline
	  id="rl-heizkreis-1"
	  points="200,30 120,30 120,183"
	  style="fill:none;stroke-width:2;stroke:rgb(0,0,255)"/>
      <line 
	  id="rl-vl-heizkreis"
	  x1="120" y1="140" x2="130" y2="140"
	  style="fill:none;stroke-width:2;stroke:rgb(0,0,255)"/>

      <!-- GEMEINSAMER RUECKLAUF -->
      <line
	  id="rl-gemeinsam"
	  x1="50" y1="183" x2="200" y2="183"
	  style="stroke-width:2;stroke:rgb(0,0,255)"/>

    </svg>


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

