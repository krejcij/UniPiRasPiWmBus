#!/usr/bin/env python
import serial
import binascii
import time
import os

# Preconditions
os.system('clear')

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
    if readedstring:
        stringedstring = binascii.hexlify(readedstring)
        parsedstring = str(stringedstring)
        temperature = parsedstring[44:45].replace("0", "") + parsedstring[45:46].replace("0", "") + parsedstring[42:43] + "." + parsedstring[43:44]
        humidity = parsedstring[54:55].replace("0", "") + parsedstring[55:56].replace("0", "") + parsedstring[52:53] + "." + parsedstring[53:54]
        increment = int(parsedstring[26:28],16)
        #rssi = int(parsedstring[98:100],16)       
        sensor_sn = parsedstring[18:20]+parsedstring[16:18]+parsedstring[14:16]+parsedstring[12:14]
        sensor_ver = parsedstring[20:22]
        sensor_type = parsedstring[22:24]
        sensor_manu = parsedstring[10:12]+parsedstring[8:10]
        sensor_manu = sensor_manu.replace("5cb0", "WEP")
        sensor_manu = sensor_manu.replace("09ee", "BON")
        
        if parsedstring[64:66]=="01": errors = "Sabotaz cidla" 
        if parsedstring[66:68]=="01": errors = "Vybita baterie"

        #signal = rssi/2-130
        signal = 0
        
        print time.strftime("%H:%M:%S %d/%m/%Y") + "    Senzor: " + sensor_manu + "." + sensor_type + "." + sensor_sn + "." + sensor_ver + "    Teplota: " + temperature + "C    Vlhkost: " + humidity + "%      RSSI: " + str(signal) + "dBm      Mereni: " + str(increment) + " "

ser.close()
f.close()
