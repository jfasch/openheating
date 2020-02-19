Thermometers
============

.. sidebar:: D-Bus

   * *Bus name*: ``{{openheating_service_def.ThermometerService.BUSNAME}}``
   * *Unit name*: ``{{openheating_service_def.ThermometerService.UNITNAME}}``
   * *Executable*: ``{{openheating_service_def.ThermometerService.EXE}}``

At the highest level, thermometers are exposed via D-Bus. The service
is implemented in the executable
:download:`/bin/openheating-thermometers.py`; responsibilities are
roughly those:

* Based on a configuration :ref:`(see below) <thermometers_config>`,
  takes care about thermometers.
* Exposes every thermometer as a D-Bus object.
* :ref:`Polls <arch_polling>` initiate a temperature read.
* Temperature reads are done in a background thread - a :doc:`Onewire
  <../faschingbauer/w1/w1>` temperature read takes over a second.
* Implements simulation mode where temperatures are read from files
  rather than real hardware. Really cool when you are on a train and
  the backpack is large enough for your laptop, but too small for an
  entire heating plant.

Objects Provided
----------------

.. csv-table::
   :header: "Object Path", "Object (Python Class)"

   {{openheating_names.ThermometerPaths.CENTER}}, :class:`openheating.dbus.thermometer_center.ThermometerCenter_Server`
   {{openheating_names.ThermometerPaths.THERMOMETER('<name>')}}, :class:`openheating.dbus.thermometer.Thermometer_Server`

.. _thermometers_config:

Sample Configuration File
-------------------------

.. literalinclude:: /installations/faschingbauer/thermometers.pyconf
    :linenos:
    :language: python
