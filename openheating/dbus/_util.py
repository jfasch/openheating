def get_object(bus, busname, path):
    return bus.get(busname, path)

def get_iface_from_object(obj, iface):
    return obj[iface]

def get_iface(bus, busname, path, iface):
    obj = get_object(bus, busname, path)
    return get_iface_from_object(obj, iface)
