from . import dbusutil

iface_name = dbusutil.DOMAIN + '.ErrorEmitter'

iface = """
<interface name='{}'>
  <signal name="error">
    <arg type="s" name="what" direction="out"/>
  </signal>
</interface>
""".format(iface_name)

