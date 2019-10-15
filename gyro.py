#!/usr/bin/python
import smbus
import math
 
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
# Necessary to activate the module
bus.write_byte_data(address, power_mgmt_1, 0)
 
print

gyroskop_xout = read_word_2c(0x43)
gyroskop_yout = read_word_2c(0x45)
gyroskop_zout = read_word_2c(0x47)
 
print "gyro_x: ", ("%5d" % gyroskop_xout), " scaleGX: ", (gyroskop_xout / 131)
print "gyro_y: ", ("%5d" % gyroskop_yout), " scaleGY:", (gyroskop_yout / 131)
print "gyro_z: ", ("%5d" % gyroskop_zout), " scaleGZ:", (gyroskop_zout / 131)
 
print

beschleunigung_xout = read_word_2c(0x3b)
beschleunigung_yout = read_word_2c(0x3d)
beschleunigung_zout = read_word_2c(0x3f)
 
beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
 
print "accel_x: ", ("%6d" % beschleunigung_xout), " scaleAX: ", beschleunigung_xout_skaliert
print "accel_y: ", ("%6d" % beschleunigung_yout), " scaleAY: ", beschleunigung_yout_skaliert
print "accel_z: ", ("%6d" % beschleunigung_zout), " scaleAZ: ", beschleunigung_zout_skaliert
 
print "X Rotation: " , get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
print "Y Rotation: " , get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert)
