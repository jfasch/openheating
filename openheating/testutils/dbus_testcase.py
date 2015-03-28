from openheating.testutils.persistent_test import PersistentTestCase

import dbus.bus
from dbus.exceptions import DBusException

import subprocess
import os.path
import time
import socket


class DBusTestCase(PersistentTestCase):
    def setUp(self):
        super().setUp()

        self.__popen = None
        self.__daemon_socket = self.rootpath() + '/my-dbus.socket'
        self.__daemon_address = 'unix:path=' + self.__daemon_socket
        self.__config_file = self.rootpath() + '/my-dbus.conf'

        config_content = _dbus_daemon_config % self.__daemon_address
        with open(self.__config_file, 'w') as f:
            f.write(config_content)

        self.start_daemon()

    def tearDown(self):
        self.stop_daemon()
        super().tearDown()

    def daemon_address(self):
        return self.__daemon_address

    def start_daemon(self):
        self.assertFalse(os.path.exists(self.__daemon_socket))
        self.assertIsNone(self.__popen)
            
        self.__popen = subprocess.Popen(['dbus-daemon', '--config-file='+self.__config_file])

        # wait until daemon has started up and socket is functional
        for i in range(100):
            if os.path.exists(self.__daemon_socket):
                break
            time.sleep(0.1)

        for i in range(100):
            with socket.socket(socket.AF_UNIX) as s:
                try:
                    s.connect(self.__daemon_socket)
                    break
                except ConnectionRefusedError:
                    continue
        
    def stop_daemon(self):
        if self.__popen is None:
            return
        self.__popen.terminate()
        self.__popen.wait()
        self.__popen = None

    def restart_daemon(self):
        self.stop_daemon()
        self.start_daemon()

    def wait_for_object(self, name, path):
        timeout = 5
        while True:
            connection = dbus.bus.BusConnection(self.daemon_address())
            try:
                the_object = connection.get_object(name, path)
                break
            except DBusException:
                timeout -= 0.1
                if timeout <= 0:
                    self.fail()
                time.sleep(0.1)


_dbus_daemon_config = '''
<!DOCTYPE busconfig PUBLIC "-//freedesktop//DTD D-Bus Bus Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd">
<busconfig>
  <!-- Our well-known bus type, don't change this -->
  <type>session</type>

  <!-- If we fork, keep the user's original umask to avoid affecting
       the behavior of child processes. -->
  <keep_umask/>
  
  <listen>%s</listen>

  <!-- allow connections from outside -->
  <auth>ANONYMOUS</auth>
  <allow_anonymous/>

  <policy context="default">
    <!-- Allow everything to be sent -->
    <allow send_destination="*" eavesdrop="true"/>
    <!-- Allow everything to be received -->
    <allow eavesdrop="true"/>
    <!-- Allow anyone to own anything -->
    <allow own="*"/>
  </policy>

  <!-- For the session bus, override the default relatively-low limits 
       with essentially infinite limits, since the bus is just running 
       as the user anyway, using up bus resources is not something we need 
       to worry about. In some cases, we do set the limits lower than 
       "all available memory" if exceeding the limit is almost certainly a bug, 
       having the bus enforce a limit is nicer than a huge memory leak. But the 
       intent is that these limits should never be hit. -->

  <!-- the memory limits are 1G instead of say 4G because they can't exceed 32-bit signed int max -->
  <limit name="max_incoming_bytes">1000000000</limit>
  <limit name="max_incoming_unix_fds">250000000</limit>
  <limit name="max_outgoing_bytes">1000000000</limit>
  <limit name="max_outgoing_unix_fds">250000000</limit>
  <limit name="max_message_size">1000000000</limit>
  <limit name="max_message_unix_fds">4096</limit>
  <limit name="service_start_timeout">120000</limit>  
  <limit name="auth_timeout">240000</limit>
  <limit name="max_completed_connections">100000</limit>  
  <limit name="max_incomplete_connections">10000</limit>
  <limit name="max_connections_per_user">100000</limit>
  <limit name="max_pending_service_starts">10000</limit>
  <limit name="max_names_per_connection">50000</limit>
  <limit name="max_match_rules_per_connection">50000</limit>
  <limit name="max_replies_per_connection">50000</limit>

</busconfig>
'''
        
