Installation
============

.. note:: 

   The entire project is not mature and well known enough to be used
   by anybody except its author, so these instructions are, well, only
   for myself.

Get the Source
--------------

Clone project,

.. code-block:: shell
	     
   (jfasch)$ git clone https://github.com/jfasch/openheating.git

Install it to ``/some/prefix``. We will refer to this directory in the
remainder of the instructions; consider it a placeholder for some
real-life installation directory like ``/usr/local`` (which is the
default if ``--prefix`` is omitted).

.. code-block:: shell
	     
   (root)$ cd openheating
   (root)$ rm -r build   # ac_subst is not re-run (bug!)
   (root)$ python3 setup.py install --prefix=/some/prefix

Bootloader
----------

My plant runs on a Raspberry, using Onewire sensors (GPIO bitbanging)
and a bunch of ordinary GPIO lines for the relays. Copy the bootloader
config over from source,

.. code-block:: shell

   (root)$ cp /some/prefix/share/installations/faschingbauer/config.txt \
		/boot/config.txt

Create User
-----------

Create `openheating` user (and give it permission to use GPIOs),

.. code-block:: shell

   (root)$ useradd --system --groups gpio openheating

OpenHeating Configuration
-------------------------

Create and fill :file:`/etc/openheating/`,

.. code-block:: shell

   (root)$ mkdir /etc/openheating
   (root)$ cp /some/prefix/share/installations/faschingbauer/thermometers.pyconf \
		/etc/openheating/
   (root)$ cp /some/prefix/share/installations/faschingbauer/switches.pyconf \
		/etc/openheating/
   (root)$ cp /some/prefix/share/installations/faschingbauer/circuits.pyconf \
		/etc/openheating/
   (root)$ cp /some/prefix/share/installations/faschingbauer/plant.pyconf \
		/etc/openheating/

.. note::

   ``plant.pyconf`` is the main config file. It defines which
   components are run, and what their config files are. So, the above
   list it a direct consequence of what's in ``plant.pyconf``.

`systemd` Unit Generator, and Plant Startup
-------------------------------------------

An OpenHeating plant consists of several independent (no, loosely
coupled) D-Bus services that are started by systemd. As the choice of
services may vary from plant to plant, the systemd service unit files
are *generated* from the ``plant.pyconf` that we copied earlier. (See
`systemd.generator(7)
<https://www.freedesktop.org/software/systemd/man/systemd.generator.html>`__
for more.)

Copy the OpenHeating unit file generator into a directory where it is
picked up by systemd,

.. code-block:: shell

   (root)$ mkdir -p /etc/systemd/system-generators
   (root)$ cp /some/prefix/bin/openheating-systemd-generator.py \
		/etc/systemd/system-generators/

The generator will be invoked, and the generated units started, after
reboot.

If you want to check that all is well, reload the configuration,

.. code-block:: shell

   (root)$ systemctl daemon-reload

and look what ``/run/systemd/generator`` contains.

HTTP Service
------------

Web is not a "component" like the others; it is currently the only
service that has a unit file to be deployed.

.. code-block:: shell

   (root)$ cp /some/prefix/share/systemd/openheating-http.service \
		/etc/systemd/system

DBus Configuration
------------------

Configure system DBus to allow us in, ::

   (root)$ cp /some/prefix/share/dbus/org.openheating.conf /etc/dbus-1/system.d/
   # systemctl reload dbus

Finally: Startup
----------------

Start necessary services, ::

   # systemctl enable openheating-http.service
   # systemctl start openheating-http.service

.. todo::

   * Generator must create necessary symlinks to start components
   * Move "startup" section to the respective installation
     instructions.

