* Intro

  * Problem

  * Alternatives

    * https://www.ta.co.at/

  * Why another heating system?

    Pictures of oil burner, wood stove, valve switch, and bloody
    off-the-shelf heating control.

  * Overview of "technologies" used

    * {lib,}gpiod

      * vs. deprecated (why?) sysfs
      * vs. RPi.GPIO @#$%^&*

    * systemd
    * D-Bus, pydbus -> "microservices" (management buy-in, especially
      with dbus interfaces defined in XML)
    * ah yes, Python (why not asyncio?)
    * Sensors: DS18x20

  * Future

    * Interoperate with legacy systems and retro protocols

      * CAN. For example,
        https://www.ta.co.at/frei-programmierbar/can-ez3/
      * Modbus. For example,
        https://www.ta.co.at/frei-programmierbar/modbus-m-bus-modul/
