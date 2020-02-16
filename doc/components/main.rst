``org.openheating.Main``
========================

.. contents::

Source
------

See :download:`/bin/openheating-main.py`

Description
-----------

Polls other components in given time intervals (default 5 seconds).

Sample Configuration File
-------------------------

Note that the configuration for the main component specifies the
layout of the entire plant. Other programs, such as
:download:`/bin/openheating-runplant.py` or
:download:`/bin/openheating-systemd-generator.py.in` read that file as
well because those are responsible for starting the components.

.. literalinclude:: /installations/faschingbauer/plant.pyconf
    :linenos:
    :language: python
