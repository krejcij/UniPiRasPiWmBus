#!/usr/bin/env python

############### Vypocitani VendorID z M-Pole ###########################################################################

def get_vendor_name(vendor_input):
    vendor_hex1 = vendor_input[2:4]
    vendor_hex2 = vendor_input[0:2]
    vendor_bin1 = bin(int(vendor_hex1, 16))[2:]
    vendor_bin2 = bin(int(vendor_hex2, 16))[2:]
    vendor_bin1 = vendor_bin1[0:8].zfill(7)
    vendor_bin2 = vendor_bin2[0:8].zfill(8)
    vendor_binary = vendor_bin1 + vendor_bin2
    vendor_letter1 = vendor_binary[0:5].zfill(5)
    vendor_letter2 = vendor_binary[5:10].zfill(5)
    vendor_letter3 = vendor_binary[10:15].zfill(5)
    vendor_char1 = int(vendor_letter1, 2) + 64
    vendor_char2 = int(vendor_letter2, 2) + 64
    vendor_char3 = int(vendor_letter3, 2) + 64
    znak1 = chr(vendor_char1)
    znak2 = chr(vendor_char2)
    znak3 = chr(vendor_char3)
    return znak1+znak2+znak3


############### Vypocitani RSSI v dBm z (-3,-4) ########################################################################

def get_signal_value(sensor_rssi):
    sensor_rssi = int(sensor_rssi)
    sensor_rssi = (sensor_rssi/2)-130
    return str(sensor_rssi)

########################################################################################################################


########################################################################################################################
########################################################################################################################
########################################################################################################################

import binascii
import time
import sqlite3
#import serial
#import os

words = []
words.append("32002e44b05c10000000021b7a660800002f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f8769")
words.append("32002e44b05c10000000021b7a670800002f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f8769")
words.append("32002e44b05c10000000021b7a680800002f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f8769")
words.append("32002e44b05c10000000021b7a690800002f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f8769")
words.append("32002e44b05c10000000021b7a700800002f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f8769")
words.append("32002e44b05c10000000021b7a710800002f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f8769")
words.append("32002e44b05c10000000021b7a720800002f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f8769")

wordLed = len(words)
for i in range(0, wordLed):
    parsedstring = str(words[i])
    temperature = parsedstring[44:45].replace("0", "") + parsedstring[45:46].replace("0", "") + parsedstring[42:43] + "." + parsedstring[43:44]
    humidity = parsedstring[54:55].replace("0", "") + parsedstring[55:56].replace("0", "") + parsedstring[52:53] + "." + parsedstring[53:54]
    increment = parsedstring[26:28]
    rssi = get_signal_value(parsedstring[98:100])
    sensor_sn = parsedstring[18:20] + parsedstring[16:18] + parsedstring[14:16] + parsedstring[12:14]
    sensor_ver = parsedstring[20:22]
    sensor_type = parsedstring[22:24]
    sensor_manu = get_vendor_name(parsedstring[8:12])


    if parsedstring[64:66] == "01": errors = "Sabotaz cidla"
    if parsedstring[66:68] == "01": errors = "Vybita baterie"

    print(time.strftime("%H:%M:%S %d/%m/%Y") + "    Mereni: " + increment + "   Senzor: " + sensor_manu + "." + sensor_type + "." + sensor_sn + "." + sensor_ver + "    Teplota: " + temperature + "C    Vlhkost: " + humidity + "%    RSSI: " + rssi + "dB")

conn = sqlite3.connect('MainDatabase.db')
print("Opened database successfully")

conn.close()


