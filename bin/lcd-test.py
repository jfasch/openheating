#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi or BeagleBone Black.
import math
import time

from openheating.hd44780 import HD44780_LCD

columns = 20

lcd = HD44780_LCD(
    rs=27,
    en=22,
    d4=25,
    d5=24,
    d6=23,
    d7=18, 
    cols=columns,
    lines=4)

while True:

    lcd.message('Hello\nworld!')
    time.sleep(1.0)
    
    # Demo showing the cursor.
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message('Show cursor')
    
    time.sleep(1.0)
    
    # Demo showing the blinking cursor.
    lcd.clear()
    lcd.blink(True)
    lcd.message('Blink cursor')
    
    time.sleep(2.0)
    
    # Stop blinking and showing cursor.
    lcd.show_cursor(False)
    lcd.blink(False)
    
    # Demo scrolling message right/left.
    lcd.clear()
    message = 'Scroll'
    lcd.message(message)
    for i in range(columns-len(message)):
    	time.sleep(0.5)
    	lcd.move_right()
    for i in range(columns-len(message)):
    	time.sleep(0.5)
    	lcd.move_left()    
