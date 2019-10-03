from . import names

iface_name = names.DOMAIN + '.ErrorEmitter'

iface = """
<interface name='{}'>
  <signal name="error">
    <arg type="s" name="what" direction="out"/>
  </signal>
</interface>
""".format(iface_name)

