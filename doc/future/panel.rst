Panel
=====

Panel
-----

The LED blinking will do most of the panel's job.

* context, maybe added as a closure in @program(). geil -> add to
  presentation.
* tests

  * count down until value on each run. program name sub(), subs an
    object contained in a closure. together with a check, maybe
    ``cmp(sub(100),0)``.
  * while loop, as a logical extension.

* next evolution step: add python code and asyncio logic. pieces
  needed.

  * read up on globals() and locals(), and lookup in general
  * python code that is run in every lauch(), taking context (global
    variables? or something that can mimic this? is there a way to
    run a coroutine with a specialized context? easily? lets own the
    dot in ... wtf ... maybe something extensible in collections?
  * task management. is there something built in to
    asyncio. routines that are available to programs.

    * asyncio.ensure_future(), have to take care of yourself. likely
	catching CancelledError and maybe do cleanup.
    * program.child(). automatic cleanup on cancel().
    * program.wait(). await launch(). geil.

  * interface. hmm. we have toplevel code objects, programs made by
    primitives in in the program module, like everything else. why
    not just add another primitive program.lauch_code(), or simply
    recognize a coroutine ??? is there an api for that, I believe
    yes!!)

    then simply await the task by adding it to one of our running
    lists. hmm. wait(). child(). fire_off() or
    asyncio.create_task().

    add these as a replacement for launch(). look into "warning"
    type exceptions. how easy that could be.

* next evolution step: marketing. on a group of buttons, pulse sine
  waves with varying frequencies.

  * forever(... hmmm .. something like ... with numpy.sine() on an
    itertools.cycle()d iterator ::

	 on(red),
	 any(
	    # blink(... sine ... rate ... frequency -> iterator!!!)
	    # -> numpy blah await asyncio.sleep(...) so geil!
	    # -> presentation
	    # think about wait() child() whatever primitives.
	    call(pyprog, *args, **kwargs))
	    wait_button(red),
	 ),
	 any(
	    blink(red, 0.5),
	    wait_button(red)
	 ),
	 # annoy a bit more
	 any(
	    blink(red. 0.1),
	    wait_button(red),
	 ),
	 
  * `@program()` should work on `range()` too? that would be the
    hammer!
  * `call(pycode)` takes a code object (in whatever precompiled
    form), `eval()` it (in whatever context, current?) and turns it
    into a program. hammer!

* play queue button, evtl. mit reset

  * task/coro started off doing a wait on a asyncio.Queue
  * maintains a task that it cancels/restarts appropriately as
    requests come in
  * requests are short programs that operate on the
    led/button/ledbutton combination

