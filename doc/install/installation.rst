Installation
============

.. note:: 

   The entire project is not mature and well known enough to be used
   by anybody except its author, so these instructions are, well, only
   for myself.

Get the Source
--------------

Clone project, and install it to `/some/prefix`,

.. code-block:: shell
	     
   (jfasch)$ git clone https://github.com/jfasch/openheating.git
   (jfasch)$ cd openheating
   (jfasch)$ python3 setup.py install --prefix=/some/prefix

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

Create `openheating` user,

.. code-block:: shell

   (root)$ useradd --system openheating

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

   :file:`plant.pyconf` is the main config file. It defines which
   components are run, and what their config files are - so the above
   list is basically an outcome of :file:`plant.pyconf`'s content.

`systemd` Unit Generator
------------------------

The components of a heating system are likely to vary from
installation to installation (despite the fact that there is only one
such installation). `systemd` unit files are *generated* from the
:file:`plant.pyconf` file that we copied earlier.

Copy the unit file generator into a directory where it is picked up by
`systemd`,

.. code-block:: shell

   (root)$ mkdir -p /etc/systemd/system-generators
   (root)$ cp /some/prefix/bin/openheating-systemd-generator.py \
		/etc/systemd/system-generators/

See `systemd.generator(7)
<https://www.freedesktop.org/software/systemd/man/systemd.generator.html>`__
for what unit file generators are.


`systemd` Units
---------------

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

