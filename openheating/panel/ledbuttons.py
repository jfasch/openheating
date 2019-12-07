from .program import LEDButton

from ..base import gpio


red = LEDButton(
    gpio.output(
        name='red_led',
        description='Red LED',
        chiplabel='pinctrl-bcm2835',
        offset=21),
    gpio.pushbutton(
        name='red_button',
        description='Red Button',
        chiplabel='pinctrl-bcm2835',
        offset=20,
        debounce_limit=0.2)
)
yellow = LEDButton(
    gpio.output(
        name='yellow_led',
        description='Yellow LED',
        chiplabel='pinctrl-bcm2835',
        offset=12),
    gpio.pushbutton(
        name='yellow_button',
        description='Yellow Button',
        chiplabel='pinctrl-bcm2835',
        offset=7,
        debounce_limit=0.2)
)
green = LEDButton(
    gpio.output(
        name='greem_led',
        description='Green LED',
        chiplabel='pinctrl-bcm2835',
        offset=24),
    gpio.pushbutton(
        name='green_button',
        description='Green Button',
        chiplabel='pinctrl-bcm2835',
        offset=23,
        debounce_limit=0.2)
)
