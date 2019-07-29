#!/usr/bin/python3

import ravel


bus = ravel.session_bus()
service = bus['org.openheating.ThermometerService']
th_service_object = service['/']
th_service_iface = th_service_object.get_interface('org.openheating.ThermometerService')

for name in th_service_iface.all_names()[0]:
    thermometer_object = th_service_iface.get_thermometer(name)
    thermometer_iface = thermometer_object.get_interface('org.openheating.Thermometer')
    print(name, thermometer_iface.get_temperature()[0])
