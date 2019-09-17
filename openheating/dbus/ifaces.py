from . import names

import ravel


class THERMOMETER:
    iface = ravel.interface(
            ravel.INTERFACE.SERVER,
            name = names.IFACE.THERMOMETER,
    )
    get_name = ravel.method(
        name = 'get_name',
        in_signature = '',
        out_signature = 's',
    )
    get_description = ravel.method(
        name = 'get_description',
        in_signature = '',
        out_signature = 's',
    )
    get_temperature = ravel.method(
        name = 'get_temperature',
        in_signature = '',
        out_signature = 'd', # double
    )

class TEMPERATURE_HISTORY:
    iface = ravel.interface(
        ravel.INTERFACE.SERVER,
        name = names.IFACE.TEMPERATURE_HISTORY)
    decision_history = ravel.method(
        name = 'decision_history',
        in_signature = '',
        out_signature = 'a(td)', # array of (uint64:timestamp,double:temperature) samples
    )
    hour_history = ravel.method(
        name = 'hour_history',
        in_signature = '',
        out_signature = 'a(td)', # array of (uint64:timestamp,double:temperature) samples
    )
    day_history = ravel.method(
        name = 'day_history',
        in_signature = '',
        out_signature = 'a(td)', # array of (uint64:timestamp,double:temperature) samples
    )

class THERMOMETER_CENTER:
    iface = ravel.interface(
        ravel.INTERFACE.SERVER,
        name = names.IFACE.THERMOMETER_CENTER)

    all_names = ravel.method(
        name = 'all_names',
        in_signature = '',
        out_signature = 'as'
    )
    
