``org.openheating.Thermometers``
================================

.. contents::

Executable
----------

:download:`/bin/openheating-thermometers.py`

Description
-----------

* Based on a :ref:`configuration <thermometers_config>`, takes care
  about thermometers.
* Exposes every thermometer as a D-Bus object.
* Polls from the :doc:`main` component initiate a temperature
  read.
* Temperature reads are done in a background thread - a :doc:`Onewire
  <../faschingbauer/w1/w1>` temperature read takes over a second.
* Implements simulation mode where temperatures are read from files
  rather than real hardware. Really cool when you are on a train and
  the backpack is too small for an entire heating plant.

Objects Provided
----------------

.. autoclass:: openheating.dbus.thermometer.Thermometer_Server
.. autoclass:: openheating.dbus.thermometer_center.ThermometerCenter_Server

.. _thermometers_config:

Sample Configuration File
-------------------------

.. literalinclude:: /installations/faschingbauer/thermometers.pyconf
    :linenos:
    :language: python
