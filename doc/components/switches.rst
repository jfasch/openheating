``org.openheating.Switches``
============================

.. contents::

Source
------

See :download:`/bin/openheating-switches.py`

Description
-----------

* Based on a :ref:`configuration <switches_config>`, takes care about
  switches.
* Exposes every switch as a D-Bus object.
* Implements simulation mode where switches are represented as files
  containing a boolean value, the switch state. Really cool when you
  are on a train and the backpack is too small for an entire heating
  plant.

.. _switches_config:

Sample Configuration File
-------------------------

.. literalinclude:: /installations/faschingbauer/switches.pyconf
    :linenos:
    :language: python
