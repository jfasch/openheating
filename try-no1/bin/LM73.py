#!/usr/bin/python

import sys, os, fcntl, struct

I2C_SLAVE = 0x0703 # from <linux/i2c-dev.h>

fd = os.open(sys.argv[1], os.O_RDWR)
fcntl.ioctl(fd, I2C_SLAVE, 0x49)

os.write(fd, '\x00')
msb_lsb = os.read(fd, 2)

msb, lsb = struct.unpack('BB', msb_lsb)
print float((msb<<24)|(lsb<<16)) / 65535 / 128

