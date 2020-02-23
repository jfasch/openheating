GLT2020 "Blink" Presentation Screenplay
=======================================

.. contents::

LED without LED
---------------

No idea what GPIO is, so I mock it up. We'll get to :ref:`libgpiod
<linkref_libgpiod>` later.

.. literalinclude:: code/led.py
   :caption: LED without nothing
   :pyobject: LED_nohw

Blocking
--------

* ``000-blink-blocking.py``: blink one LED, using blocking
  time.sleep() in the middle
* ``001-blink-multiple-mt.py``: blink multiple LEDs. Like above, but
  multiple threads.

.. todo::

   Write those

Discussion: hmm, multithreading

* thread termination
* cache thrashing
* locking?

`asyncio` Basics
----------------

``010-asyncio-basics.py``
.........................

.. literalinclude:: code/010-asyncio-basics.py

Discussion: 

* Aha: async, await
* View with `strace`
* Discuss epoll (select, poll)

``020-asyncio-parallel.py``
...........................

.. literalinclude:: code/020-asyncio-parallel.py

Discussion:

* Aha, parallel, whats that?
* strace: look ma, *no* multithreading
* Discuss *cooperative multitasking*

  * Doze 3.11
  * No-one should *block*

Towards Functional
------------------

``030-sos.py``
..............

**SOS**

* 3 times fast
* 3 times slow
* 3 times fast

.. literalinclude:: code/030-sos.py

Discussion:

* Nothing really new here
* Next: *SOS* in a loop, with sleep in between.
* But first: LEDs in a terminal aren't so sexy
  
  * Introduce GPIO

GPIO
----

.. todo::

   Discuss ``RPi.GPIO``

   * purely Raspi specific
   * Used to map ``/dev/mem`` -> required root permission
   * Uses ``/dev/gpiomem`` nowadays -> group gpio (ok)
   * Events: fired from background thread. Outright crap.

.. todo::

   Discuss sysfs gpio

   * File based interface -> simple
   * But ...

     * Events from ``value`` file -> have to read fast enough when
       edge is important
     * No event *buffering* -> event loss
     * unmaintained

.. todo::

   Discuss :ref:`libgpiod <linkref_libgpiod>`

   * Complicated set of ioctls
   * Userspace C library
   * Associated programs 

     * Demo

   * Binding for Python and C++

.. todo::

   loop.add_reader() -> events

``040-sos-loop-error.py``
.........................

.. literalinclude:: code/040-sos-loop-error.py

.. todo::

   Use GPIO LED from now on

Error:

.. code-block:: shell

   $ ./040-sos-loop-error.py 
   on
   ... SOS here ...
   off
   Traceback (most recent call last):
     File "./040-sos-loop-error.py", line 33, in <module>
       loop.run_until_complete(forever(sos(led)))
     File "/usr/lib64/python3.7/asyncio/base_events.py", line 583, in run_until_complete
       return future.result()
     File "./040-sos-loop-error.py", line 28, in forever
       await coro
   RuntimeError: cannot reuse already awaited coroutine

Discussion:

* ``forever()``. problem: coroutine can only be awaited once. discuss
  coroutines, yield?, return (-> coroutine termination)
* Aha: need a factory that can "re"create coros

Towards Functional, Continued
-----------------------------

Decorators: Simple Example
..........................

.. literalinclude:: code/050-decorator.py

Discussion:

* magic: "@". Same as saying ``debug(hypotenuse)``
* ``wrapper`` *wraps* ``fun``
* ``fun`` is said to be *in the closure*

More evident closure:

.. code-block:: python

   >>> def hardwired_printer(*args, **kwargs):
   ...     def _print():
   ...             print('args', args, 'kwargs', kwargs)
   ...     return _print
   ... 
   >>> p1 = hardwired_printer(1, 2, 3)
   >>> p1
   <function hardwired_printer.<locals>._print at 0x7fb31dcf18c0>
   >>> p1()
   args (1, 2, 3) kwargs {}
   >>> 
   >>> p2 = hardwired_printer(666, answer=42)
   >>> p2()
   args (666,) kwargs {'answer': 42}

``060-program-decorator.py``
............................

So what's the problem?

* ``sos()`` terminates -> cannot await it a second time

Solution:

* Need something that *remembers* the parameters -> decorator
* That something must be "launchable"

.. literalinclude:: code/060-program-decorator.py

Entire Library of Such Programs
-------------------------------

.. literalinclude:: /openheating/panel/program.py
   :pyobject: sequence

.. literalinclude:: /openheating/panel/program.py
   :pyobject: n_times

.. literalinclude:: /openheating/panel/program.py
   :pyobject: forever

.. literalinclude:: /openheating/panel/program.py
   :pyobject: all

.. literalinclude:: /openheating/panel/program.py
   :pyobject: any

.. literalinclude:: /openheating/panel/program.py
   :pyobject: wait_button

Easy Programming
----------------

Examples ...

.. code-block:: python

   forever(any(sleep(3), blink(0.2, green.led)),
           any(sleep(3), blink(0.2, yellow.led)),
           any(sleep(3), blink(0.2, red.led)))

Push-Button Events
------------------

.. todo::

   * Live-hacking: debounce buttons
   * wait_button()
   * subprocess_shell()
   * http_get()
   * blink.open_url()
