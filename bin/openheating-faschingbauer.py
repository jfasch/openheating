#!/usr/bin/python3

from openheating.test.plant import Plant


class FaschingbauerPlant(Plant):
    def __init__(self):
        super().__init__(
            [
                service.ThermometerService(
                    pyconf=[
                        "from openheating.base.w1 import W1Thermometer",

                        "THERMOMETERS = [",
                        "    W1Thermometer('Raum', 'Raum', '/sys/bus/w1/devices/28-02131dc603aa'),",

                        "    W1Thermometer('SpeicherOben', 'Speicher Oben', '/sys/bus/w1/devices/28-011432f138f9'),",
                        "    W1Thermometer('SpeicherMitte', 'Speicher Mitte', '/sys/bus/w1/devices/28-01131676b23f'),",
                        "    W1Thermometer('SpeicherUnten', 'Speicher Unten', '/sys/bus/w1/devices/28-02131df83daa'),",
                        "    W1Thermometer('RuecklaufSolar', 'Ruecklauf Solar', '/sys/bus/w1/devices/28-02131d96bbaa'),",
                        "    W1Thermometer('VorlaufSolar', 'Vorlauf Solar', '/sys/bus/w1/devices/28-02131d959eaa'),",

                        "    W1Thermometer('Oelbrenner', 'Oelbrenner', '/sys/bus/w1/devices/28-02131d676baa'),",

                        "    W1Thermometer('Holzbrenner', 'Holzbrenner', '/sys/bus/w1/devices/28-01131676d067'),",
                        "    W1Thermometer('RuecklaufHolz', 'Ruecklauf Holz', '/sys/bus/w1/devices/28-011432772cf9'),",
                        "    W1Thermometer('VorlaufHolz', 'Vorlauf Holz', '/sys/bus/w1/devices/28-02131dfd21aa'),",

                        "    W1Thermometer('VorlaufHeizkreis', 'Vorlauf Heizkreis', '/sys/bus/w1/devices/28-02131dace9aa'),",
                        "    W1Thermometer('VorlaufWarmwasser', 'Vorlauf Warmwasser', '/sys/bus/w1/devices/28-02131d9920aa'),",
                        "]",
                    ],
                    update_interval=5),
                service.SwitchService(
                    pyconf=[
                        "from openheating.base import gpio",

                        "_pins = [",
                        "    (17, None, None),",
                        "    (27, None, None),",
                        "    (22, None, None),",
                        "    (10, None, None),",
                        "    ( 9, None, None),",
                        "    (11, None, None),",
                        "    (13, None, None),",
                        "    (19, None, None),",
                        "    (18, None, None),",
                        "    (23, None, None),",
                        "    (24, None, None),",
                        "    (25, None, None),",
                        "    (12, None, None),",
                        "    (16, None, None),",
                        "    (20, None, None),",
                        "    (21, None, None),",
                        "]",
                        "SWITCHES = [",
                        "    gpio.output(name = name or 'Relay_{}'.format(seq),",
                        "                description = description or 'Relay #{} on pin #{}'.format(seq, pin),",
                        "                chiplabel = 'pinctrl-bcm2835',",
                        "                offset = pin,",
                        "    )",
                        "    for seq, (pin, name, description) in enumerate(_pins)",
                        "]",
                    ]),
                service.CircuitService(
                    pyconf=[
                        'from openheating.base.circuit import Circuit',
                        'from openheating.dbus.thermometer_center import ThermometerCenter_Client',
                        'from openheating.dbus.switch_center import SwitchCenter_Client',

                        'thermometer_center = ThermometerCenter_Client(bus=BUS)',
                        'switch_center = SwitchCenter_Client(bus=BUS)',
                        'speicheroben_thermometer = thermometer_center.get_thermometer("SpeicherOben")',
                        'holzbrenner_thermometer = thermometer_center.get_thermometer("Holzbrenner")',
                        'hk_switch = switch_center.get_switch("hk")',
                        
                        'CIRCUITS = [',
                        '   Circuit("HK", "Heizkreis",',
                        '           pump=hk_switch, producer=holzbrenner_thermometer, consumer=speicheroben_thermometer,',
                        '           diff_low=3, diff_high=10)',
                        ']',
                    ]),
            ])
        

