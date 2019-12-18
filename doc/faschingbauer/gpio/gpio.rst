GPIO
====

Boot Loader Config
------------------

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
not, from power on until I configure them in
openheating-switches.py. To keep the duration with undefined state at
a minimum, in `/boot/config.txt` you write ::

  # "op" ... output
  # "dl" ... drive low
  gpio=17=op,dl
  gpio=27=op,dl
  gpio=22=op,dl
  gpio=5=op,dl
  gpio=6=op,dl
  gpio=13=op,dl
  gpio=19=op,dl
  gpio=26=op,dl
  gpio=14=op,dl
  gpio=15=op,dl
  gpio=18=op,dl
  gpio=7=op,dl
  gpio=12=op,dl
  gpio=16=op,dl
  gpio=20=op,dl
  gpio=21=op,dl
