DBUS_BASE_ENTRIES = ['org', 'openheating']
DBUS_THERMOMETER_IFACE_ENTRIES = DBUS_BASE_ENTRIES + ['Thermometer']
DBUS_THERMOMETER_IFACE_STRING = '.'.join(DBUS_THERMOMETER_IFACE_ENTRIES)

def dbus_thermometer_object_name_path(thname):
    entries = DBUS_THERMOMETER_IFACE_ENTRIES + [thname]
    return '.'.join(entries), '/'.join([''] + entries)
