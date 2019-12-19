GPIO
====

Using Built-In GPIOs
--------------------

Sainsmart relay boards operate at 5V, the Raspi IOs do so at
3.3V. Using BC548C and two resistors to handle that; see jjj for a
diagram.

Anyway: the GPIOs POR direction is "in", apparently (didn't check the
datasheet but it makes sense). I have no idea 

* what level a GPIO, when configured as "in", is supposed to see on a
  transistor's base
* how the transistor behaves if its base is connected to a GPIO
  configured as "in"

The effect of all this is that some relays are switched and some are
not.

* Beginners (i.e. myself) reading:
  https://embeddedartistry.com/blog/2018/06/04/demystifying-microcontroller-gpio-settings/

* Processor datasheet excerpt, regarding GPIOs:
  https://elinux.org/RPi_BCM2835_GPIOs

  Most interesting being the different pullup/down POR configurations
  of the pins which explain the effects that I see. For example, GPIO
  5 and 6 tend to rebel - as the table shows, these are configured as
  pullup, so applying a pull-down resistor is rather
  counterproductive.

  Original datasheet; see page 100ff, "GPIO Pull-up/down Register
  (GPPUD)":
  http://www.raspberrypi.org/wp-content/uploads/2012/02/BCM2835-ARM-Peripherals.pdf

  Note also the sentence at the bottom of page 100, "The Alternate
  function table also has the pull state which is applied after a
  power down." So, the states listed there are the POR states of the
  respective IOs.

Using MCP23017
--------------

MCP23017 is a I2C/SPI IO expander. Easily attached (see for example
http://www.faschingbauer.co.at/de/howtos/gpio-mcp23017/, but dont
forget to connect RESET to 3V3 :-) )

Issues:

* (using gpiod) closing the chip fd does not reset pins to their POR
  state. Unusable. This is likely the driver's fault.
* CPU reset does not propagate to MCP23017. Unusable.
