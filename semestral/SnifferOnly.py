#!/usr/bin/env python
import serial
import binascii
import time
import os

# Setup a serial port
ser = serial.Serial(
  port='/dev/ttyAMA0',
  baudrate = 19200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)
print "Device is on AMA0: " + str(ser.isOpen())

# Wake up device
ser.write("\x00\x00")
print "Device is waked up: True"

# Set as a sniffer
ser.write("\x00\x00>0a:01\x0D")
z = ser.readline()
print "Device is set as Sniffer T: " + z

# Sniff all packets
f = open('cteni_sniffer.txt','w')
print "Sniffing now:"
print ""

while True:
    readedstring = ser.read(51)
    stringedstring = binascii.hexlify(readedstring)
    parsedstring = str(stringedstring)
    if readedstring:
        f.write(parsedstring + '\n')
        print parsedstring

ser.close()
f.close()
