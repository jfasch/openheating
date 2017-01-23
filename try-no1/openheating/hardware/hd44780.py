# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
# Original project URL: https://github.com/adafruit/Adafruit_Python_CharLCD.git

# Modified (c) 2014 Joerg Faschingbauer: rip out dependencies,
# backlight, and use my own GPIO based on sysfs (don't want to run as
# root).

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from . import gpio

import time

# Commands
LCD_CLEARDISPLAY        = 0x01
LCD_RETURNHOME          = 0x02
LCD_ENTRYMODESET        = 0x04
LCD_DISPLAYCONTROL      = 0x08
LCD_CURSORSHIFT         = 0x10
LCD_FUNCTIONSET         = 0x20
LCD_SETCGRAMADDR        = 0x40
LCD_SETDDRAMADDR        = 0x80

# Entry flags
LCD_ENTRYRIGHT          = 0x00
LCD_ENTRYLEFT           = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Control flags
LCD_DISPLAYON           = 0x04
LCD_DISPLAYOFF          = 0x00
LCD_CURSORON            = 0x02
LCD_CURSOROFF           = 0x00
LCD_BLINKON             = 0x01
LCD_BLINKOFF            = 0x00

# Move flags
LCD_DISPLAYMOVE         = 0x08
LCD_CURSORMOVE          = 0x00
LCD_MOVERIGHT           = 0x04
LCD_MOVELEFT            = 0x00

# Function set flags
LCD_8BITMODE            = 0x10
LCD_4BITMODE            = 0x00
LCD_2LINE               = 0x08
LCD_1LINE               = 0x00
LCD_5x10DOTS            = 0x04
LCD_5x8DOTS             = 0x00

# Offset for up to 4 rows.
LCD_ROW_OFFSETS         = (0x00, 0x40, 0x14, 0x54)

# Char LCD plate GPIO numbers.
LCD_PLATE_RS            = 15
LCD_PLATE_RW            = 14
LCD_PLATE_EN            = 13
LCD_PLATE_D4            = 12
LCD_PLATE_D5            = 11
LCD_PLATE_D6            = 10
LCD_PLATE_D7            = 9
LCD_PLATE_RED           = 6
LCD_PLATE_GREEN         = 7
LCD_PLATE_BLUE          = 8

# Char LCD plate button names.
SELECT                  = 0
RIGHT                   = 1
DOWN                    = 2
UP                      = 3
LEFT                    = 4

class HD44780_LCD(object):
    """Class to represent and interact with an HD44780 character LCD display."""

    def __init__(self, rs, en, d4, d5, d6, d7, cols, lines):
        self.__cols = cols
        self.__lines = lines
        self.__rs = gpio.create(rs)
        self.__en = gpio.create(en)
        self.__d4 = gpio.create(d4)
        self.__d5 = gpio.create(d5)
        self.__d6 = gpio.create(d6)
        self.__d7 = gpio.create(d7)

        # Setup all pins as outputs.
        for pin in (self.__rs, self.__en, self.__d4, self.__d5, self.__d6, self.__d7):
            pin.set_direction(gpio.OUT)

        # Initialize the display.
        self.write8(0x33)
        self.write8(0x32)
        # Initialize display control, function, and mode registers.
        self.displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.displayfunction = LCD_4BITMODE | LCD_1LINE | LCD_2LINE | LCD_5x8DOTS
        self.displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
        # Write registers.
        self.write8(LCD_DISPLAYCONTROL | self.displaycontrol)
        self.write8(LCD_FUNCTIONSET | self.displayfunction)
        self.write8(LCD_ENTRYMODESET | self.displaymode)  # set the entry mode
        self.clear()

    def home(self):
        """Move the cursor back to its home (first line and first column)."""
        self.write8(LCD_RETURNHOME)  # set cursor position to zero
        self.__delay_microseconds(3000)  # this command takes a long time!

    def clear(self):
        """Clear the LCD."""
        self.write8(LCD_CLEARDISPLAY)  # command to clear display
        self.__delay_microseconds(3000)  # 3000 microsecond sleep, clearing the display takes a long time

    def set_cursor(self, col, row):
        """Move the cursor to an explicit column and row position."""
        # Clamp row to the last row of the display.
        if row > self.__lines:
            row = self.__lines - 1
        # Set location.
        self.write8(LCD_SETDDRAMADDR | (col + LCD_ROW_OFFSETS[row]))

    def enable_display(self, enable):
        """Enable or disable the display.  Set enable to True to enable."""
        if enable:
            self.displaycontrol |= LCD_DISPLAYON
        else:
            self.displaycontrol &= ~LCD_DISPLAYON
        self.write8(LCD_DISPLAYCONTROL | self.displaycontrol)

    def show_cursor(self, show):
        """Show or hide the cursor.  Cursor is shown if show is True."""
        if show:
            self.displaycontrol |= LCD_CURSORON
        else:
            self.displaycontrol &= ~LCD_CURSORON
        self.write8(LCD_DISPLAYCONTROL | self.displaycontrol)

    def blink(self, blink):
        """Turn on or off cursor blinking.  Set blink to True to enable blinking."""
        if blink:
            self.displaycontrol |= LCD_BLINKON
        else:
            self.displaycontrol &= ~LCD_BLINKON
        self.write8(LCD_DISPLAYCONTROL | self.displaycontrol)

    def move_left(self):
        """Move display left one position."""
        self.write8(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)

    def move_right(self):
        """Move display right one position."""
        self.write8(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)

    def set_left_to_right(self):
        """Set text direction left to right."""
        self.displaymode |= LCD_ENTRYLEFT
        self.write8(LCD_ENTRYMODESET | self.displaymode)

    def set_right_to_left(self):
        """Set text direction right to left."""
        self.displaymode &= ~LCD_ENTRYLEFT
        self.write8(LCD_ENTRYMODESET | self.displaymode)

    def autoscroll(self, autoscroll):
        """Autoscroll will 'right justify' text from the cursor if set True,
        otherwise it will 'left justify' the text.
        """
        if autoscroll:
            self.displaymode |= LCD_ENTRYSHIFTINCREMENT
        else:
            self.displaymode &= ~LCD_ENTRYSHIFTINCREMENT
        self.write8(LCD_ENTRYMODESET | self.displaymode)

    def message(self, text):
        """Write text to display.  Note that text can include newlines."""
        line = 0
        # Iterate through each character.
        for char in text:
            # Advance to next line if character is a new line.
            if char == '\n':
                line += 1
                # Move to left or right side depending on text direction.
                col = 0 if self.displaymode & LCD_ENTRYLEFT > 0 else self.__cols-1
                self.set_cursor(col, line)
            # Write the character to the display.
            else:
                self.write8(ord(char), True)

    def write8(self, value, char_mode=False):
        """Write 8-bit value in character or data mode.  Value should be an int
        value from 0-255, and char_mode is True if character data or False if
        non-character data (default).
        """
        # One millisecond delay to prevent writing too quickly.
        self.__delay_microseconds(1000)
        # Set character / data bit.
        self.__rs.set_value(char_mode)
        # Write upper 4 bits.
        self.__d4.set_value(((value >> 4) & 1) > 0)
        self.__d5.set_value(((value >> 5) & 1) > 0)
        self.__d6.set_value(((value >> 6) & 1) > 0)
        self.__d7.set_value(((value >> 7) & 1) > 0)
        self.__pulse_enable()

        # Write lower 4 bits.
        self.__d4.set_value((value        & 1) > 0)
        self.__d5.set_value(((value >> 1) & 1) > 0)
        self.__d6.set_value(((value >> 2) & 1) > 0)
        self.__d7.set_value(((value >> 3) & 1) > 0)
        self.__pulse_enable()


    def __delay_microseconds(self, microseconds):
        # Busy wait in loop because delays are generally very short (few microseconds).
        end = time.time() + (microseconds/1000000.0)
        while time.time() < end:
            pass

    def __pulse_enable(self):
        # Pulse the clock enable line off, on, off to send command.
        self.__en.set_value(False)
        self.__delay_microseconds(1)       # 1 microsecond pause - enable pulse must be > 450ns
        self.__en.set_value(True)
        self.__delay_microseconds(1)       # 1 microsecond pause - enable pulse must be > 450ns
        self.__en.set_value(False)
        self.__delay_microseconds(1)       # commands need > 37us to settle
