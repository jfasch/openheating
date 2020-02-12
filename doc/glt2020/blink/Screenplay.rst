Functional Programming with `asyncio` and `libgpiod`
====================================================

`asyncio` Basics
----------------

* `000-blink-blocking.py`
* `001-blink-multiple-mt.py`

* `010-asyncio-basics.py`

  * Aha: async, await
  * View with `strace`
  * Discuss epoll (select, poll)

* `020-asyncio-parallel.py` (LED += color, indent)

  * Aha, parallel
  * strace: *no* multithreading
  * Discuss *cooperative multitasking*

    * Doze 3.11
    * No-one should *block*

* SOS, in a loop, eventually

  * SOS: 3 times fast, three times slow, three times fast -> one
    routine, `sos()`
  * `030-sos.py`: linear sequence, SOS. one run, terminate fine.
  * `040-sos-loop-error.py`: loop around SOS ... hmm
      ... `forever()`. problem: coroutine can only be awaited
      once. discuss coroutines, yield?, return (-> coroutine
      termination)
  * Aha: need a factory instead that can "re"create coros
  
* Decorators

  * 050-decorator.py

* `060-program-decorator.py`

  * three stage decorator. will they understand?
  * start small: decorate sos and run it
  * forever: launches program manually (wrap into ensure_future;
    discuss)
  * helper function launch()
