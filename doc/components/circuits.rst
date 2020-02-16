``org.openheating.Circuits``
============================

.. contents::

Source
------

See :download:`/bin/openheating-circuits.py`

Description
-----------

* Uses two thermometers, producer and consumer.
* The temperature difference acts as input for a hysteresis; based on
  the difference the controlled pump (via a relay) is switched on and
  off.

.. _circuits_config:

Sample Configuration File
-------------------------

.. literalinclude:: /installations/faschingbauer/circuits.pyconf
    :linenos:
    :language: python
