#!/usr/bin/env python
# -*- coding: utf-8 -*-
import binascii
import time
import sys, getopt

global db
global file
global demo_run
global AES_IQRF_KLIC_DEMO_TELEGRAMU
AES_IQRF_KLIC_DEMO_TELEGRAMU = 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'

try:
    from Crypto.Cipher import AES
except ImportError:
    print("FATAL ERROR: PyCrypto module not found !")
    exit(1)
try:
    import sqlite3
except ImportError:
    print("FATAL ERROR: SQite3 module not found !")
    exit(1)
try:
    import serial
except ImportError:
    print("FATAL ERROR: Serial module not found !")
    demo_run = True
############ Vypis hodnoty dle LSB #####################################################################################
def LSB(bytes):
    new = ""
    size = len(bytes)
    while (size > 0):
        new = new + bytes[size - 2:size]
        size = size - 2
    return new

############ Logovani do souboru #######################################################################################
def log(log):
    file.write(bytes(time.strftime("%d/%m/%Y  %H:%M:%S  ") + log + "\n", 'UTF-8'))
    return

############ Databazovy zapis ##########################################################################################
def sql(query):
    db.execute(query)
    db.commit()
    output(query)
    return

############ Obecny vystup #############################################################################################
def output(output):
    log(output)
    print(time.strftime("%d/%m/%Y  %H:%M:%S  ") + output)
    return

############ Parsovani jednotliveho telegramu ##########################################################################
def parse_telegram(parsedstring,RunType):
    output("Received telegram: " + parsedstring)
    errors = ''
    sensor_sn = LSB(parsedstring[12:20])
    sensor_ver = parsedstring[20:22]
    sensor_type = parsedstring[22:24]
    sensor_manu = get_vendor_name(parsedstring[8:12])
    device = parsedstring[8:24].upper()

    increment = str(int(parsedstring[26:28], 16)).rjust(3, ' ')
    access = str(parsedstring[26:28])
    rssi = get_signal_value(parsedstring[-4:-2])

    if(demo_run != True):
        # Get actual IQRF key
        ser.write("\x00\x00>03?\x0D")
        AES_KEY_IQRF = ser.readline()
        output("Actual AES key is: " + AES_KEY_IQRF[1:].upper())
    else:
        AES_KEY_IQRF = binascii.unhexlify(AES_IQRF_KLIC_DEMO_TELEGRAMU) #DEFAULT AES IQRF KEY
        sql("INSERT INTO TELEGRAMS (DATETIME,PRE,HEADER,DATA,POST,AESKEY) VALUES ('"+time.strftime("%Y-%m-%d %H:%M")+"', '"+parsedstring[0:4]+"', '"+parsedstring[4:34]+"', '"+parsedstring[34:-4]+"', '"+parsedstring[-4:]+"','"+AES_IQRF_KLIC_DEMO_TELEGRAMU+"')")

    ############ Rozsifrujeme zasifrovany telegram #####################################################################
    configuration_field = parsedstring[33:34]
    if (configuration_field == '5'):
        aes = True

        # Nacti sifrovanou cast dat z prichoziho paketu
        TELEGRAM_DECRYPTED = binascii.unhexlify(parsedstring[34:-4])
        # Nacti prislusny sifrovaci klic daneho zarizeni z DB
        vysledky = db.execute("SELECT `DEVICE_AES` FROM `DEVICES` WHERE `DEVICE_ADDRESS` LIKE '%"+device+"%' LIMIT 1;")
        vysledek = vysledky.fetchone()
        AES_KEY_DEVICE = binascii.unhexlify(vysledek[0])
        # Sestav inicializacni vektor z prichoziho paketu
        AES_IV=binascii.unhexlify(device+access*8)

        # Vsechno nad velkymi pismeny
        binascii.hexlify(AES_IV).upper()
        binascii.hexlify(AES_KEY_IQRF).upper()
        binascii.hexlify(AES_KEY_DEVICE).upper()
        binascii.hexlify(TELEGRAM_DECRYPTED).upper()

        # Vem telegram rozsifrovany univerzalnim klicem (AES klic zadany v IQRF) a zpet ho s nim zasifruj. Dostaneme sprave prenaseny telegram.
        if (RunType!='aes_clean'):
            encryptor_back = AES.new(AES_KEY_IQRF, AES.MODE_CBC, IV=AES_IV)
            TELEGRAM_CRYPTED = encryptor_back.encrypt(TELEGRAM_DECRYPTED)
        else:
            TELEGRAM_CRYPTED = TELEGRAM_DECRYPTED

        # Ten ted rozsifrujeme spravnym klicem (AES klic daneho zarizeni), dostaneme nesifrovana data.
        encryptor_new = AES.new(AES_KEY_DEVICE, AES.MODE_CBC, IV=AES_IV)
        TELEGRAM_ORIGINAL = encryptor_new.decrypt(TELEGRAM_CRYPTED)

        # Pro kontrolu to vypiseme
        print(bytes("AES_IV: ",'UTF-8')+binascii.hexlify(AES_IV))
        print(bytes("AES_DEVICE: ",'UTF-8')+binascii.hexlify(AES_KEY_DEVICE))
        print(bytes("AES_TEL_DECRYPTED: ",'UTF-8')+binascii.hexlify(TELEGRAM_DECRYPTED))
        print(bytes("AES_TEL_CRYPTED: ",'UTF-8')+binascii.hexlify(TELEGRAM_CRYPTED))
        print(bytes("AES_TEL_ORIGINAL: ",'UTF-8')+binascii.hexlify(TELEGRAM_ORIGINAL))

        aes_control = binascii.hexlify(TELEGRAM_ORIGINAL[0:2]).upper()
        if (aes_control != b'2F2F'):
            output("ERROR: nelze desifrovat paket " + str(binascii.hexlify(TELEGRAM_DECRYPTED).upper()))
            return
        else:
            parsedstring = parsedstring[0:34] + str(
                binascii.hexlify(TELEGRAM_ORIGINAL).upper().decode('ascii')) + parsedstring[-4:]
            # print(parsedstring)

    else:
        aes = False

    ############ Vyparsujeme potrebne informace ########################################################################
    if (sensor_manu == "WEP"):
        if parsedstring[66:68] == "01": errors = "Vybita baterie"
        temperature = parsedstring[44:45].replace("0", "") + parsedstring[45:46].replace("0", "") + parsedstring[42:43] + "." + parsedstring[43:44]
        humidity = parsedstring[54:55].replace("0", "") + parsedstring[55:56].replace("0", "") + parsedstring[
                                                                                                 52:53] + "." + parsedstring[
                                                                                                                53:54]
        sql("INSERT INTO MEASURES (DATETIME,DEVICE,RSSI,TYPE1,VALUE1,TYPE2,VALUE2) VALUES ('" + time.strftime(
            "%Y-%m-%d %H:%M") + "', '" + device + "', '" + rssi + "', '°C', '" + temperature + "','%','"+humidity+"')")
        output(
            "Mereni: " + increment + "  Senzor: " + sensor_manu + "." + sensor_type + "." + sensor_sn + "." + sensor_ver + "    RSSI: " + rssi + "dB     AES: " + str(
                aes).ljust(5, ' ') + "   Teplota: " + temperature.rjust(5, ' ') + "°C    Vlhkost: " + humidity.rjust(5,
                                                                                                                     ' ') + "%     " + errors)
    elif (sensor_manu == "BON"):
        Spotreba = str(int(LSB(parsedstring[42:46]), 16))
        Cascteni = get_date(LSB(parsedstring[58:62])) + " " + get_time(LSB(parsedstring[54:58]))

        sql("INSERT INTO MEASURES (DATETIME,DEVICE,RSSI,TYPE1,VALUE1,TYPE2,VALUE2) VALUES ('" + time.strftime(
            "%Y-%m-%d %H:%M") + "', '" + device + "', '" + rssi + "', 'l', '" + Spotreba + "','Odecet','"+Cascteni+"')")
        output(
            "Mereni: " + increment + "  Senzor: " + sensor_manu + "." + sensor_type + "." + sensor_sn + "." + sensor_ver + "    RSSI: " + rssi + "dB     AES: " + str(
                aes).ljust(5, ' ') + "   Spotřeba: " + Spotreba.rjust(7, ' ') + "l    Cas: " + Cascteni + errors)
    elif (sensor_manu == "KAM"):
        #DobaBehu = int(LSB(parsedstring[42:50]),16)
        #Prurez1 = int(LSB(parsedstring[54:62]), 16)
        Prutok = str(int(LSB(parsedstring[66:74]), 16))
        # RozsirujiciChyby print(parsedstring[80:84])
        Teplota1 = str(int(LSB(parsedstring[88:92]), 16)/100)
        DatumCas1 = get_date(LSB(parsedstring[96:100]))
        DatumCas2 = get_date(LSB(parsedstring[104:108]))
        #Prurez2 = int(LSB(parsedstring[112:120]), 16)
        Energie1 = str(int(LSB(parsedstring[124:132]), 16)*10)
        Teplota2 = str(int(LSB(parsedstring[136:140]), 16)/100)
        #KamstupSpecific print(parsedstring[146:154])
        #KamstrupSpecific print(parsedstring[158:166])
        Energie2 = str(int(LSB(parsedstring[172:180]), 16)*10)
        # KAMSTRUP aktualne neukladame z duvodu dlouhodobeho rizeneho neotestovani
        # sql("INSERT INTO MEASURES (DATETIME,DEVICE,RSSI,TYPE1,VALUE1,TYPE2,VALUE2) VALUES ('" + time.strftime("%Y-%m-%d %H:%M") + "', '" + device + "', '" + rssi + "', 'Wh', '" + value1 + "','Wh','"+value2+"')")
        output(
            "Mereni: " + increment + "  Senzor: " + sensor_manu + "." + sensor_type + "." + sensor_sn + "." + sensor_ver + "    RSSI: " + rssi + "dB     AES: " + str(
                aes).ljust(5, ' ') + "   Teplota: " + Teplota1 +"/"+ Teplota2 + "°C   Energie: " + Energie1 + "/" + Energie2 + "MJ  Prutok: " + Prutok +"m3/hod"  + errors)

    elif (sensor_manu == "ZPA"):
        Spotreba1 = str(int(LSB(parsedstring[58:70]), 16)/1000)
        Spotreba2 = str(int(LSB(parsedstring[78:88]), 16)/1000)
        sql("INSERT INTO MEASURES (DATETIME,DEVICE,RSSI,TYPE1,VALUE1,TYPE2,VALUE2) VALUES ('" + time.strftime(
            "%Y-%m-%d %H:%M") + "', '" + device + "', '" + rssi + "', 'kWh', '" + Spotreba1 + "','kWh','"+Spotreba2+"')")
        output(
            "Mereni: " + increment + "  Senzor: " + sensor_manu + "." + sensor_type + "." + sensor_sn + "." + sensor_ver + "    RSSI: " + rssi + "dB     AES: " + str(
                aes).ljust(5, ' ') + "   Spotreba T1: " + Spotreba1 + "kWh   Spotreba T2: " + Spotreba2 + "kWh" + errors)
    else:
        output(
            "Mereni: " + increment + "  Senzor: " + sensor_manu + "." + sensor_type + "." + sensor_sn + "." + sensor_ver + "    RSSI: " + rssi + "dB     AES: " + str(
                aes).ljust(5, ' ') + "   Telegram structure not supported. " + errors)
    return

############################ Vypocitani data ve formatu G ##############################################################
def get_date(date_bytes):
    date = str(bin(int(date_bytes[0:2], 16))[2:]).zfill(8) + str(bin(int(date_bytes[2:4], 16))[2:]).zfill(8)
    year = str(int(date[0:4]+date[8:11], 2))
    month = str(int(date[4:8], 2))
    day = str(int(date[11:16], 2))
    vysledek = day + "." + month + ".20" + year
    return vysledek

############################ Vypocitani casu ve formatu F ##############################################################
def get_time(time_bytes):
    time = str(bin(int(time_bytes[0:2], 16))[2:]).zfill(8) + str(bin(int(time_bytes[2:4], 16))[2:]).zfill(8)
    hour = str(int(time[3:8], 2))
    minute = str(int(time[10:16], 2)).zfill(2)
    vysledek = hour + ":" + minute
    return vysledek

############### Vypocitani VendorID z M-Pole ###########################################################################
def get_vendor_name(vendor_input):
    # !!! toto chce refaktor!
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
    return znak1 + znak2 + znak3

############### Demonstracni hodnoty telegramu pro offline ukazku ci testy #############################################
def get_demo_telegrams(demo_type):
    words = []

    if (demo_type == "aes_iqrf"):
        # BONEGA AES
        words.append("22001E44EE092101000001067AED00100546027F366AB9B77C8AF39ED0E483CFDF1234")  # ME
        words.append("22001E44EE092101000001077AEE001005308C0D6214F75FCB1C92B247AA2BBB481234")  # ME
        words.append("22001E44EE092101000001067AEE001005D8B29F90ADA53B75D6E0A882AF0B62E41234")  # ME
        words.append("22001E44EE092101000001077AEF0010052751EC0CB5EE06339F4610E564554A8E1234")  # ME
        words.append("22001E44EE092101000001067AEF001005FDC98128F488C529F8F0A2CB9EE25EF81234")  # ME
        words.append("22001E44EE092101000001077AF0001005CB79F8422323895DA8C0FA7185B9B80B1234")  # ME
        # WEPTECH AES
        words.append("32002E44B05C10000000021B7A0618200517BEC2259D319C81004EC1C65366CF3FAACD81C07774C950761CEC51AE26E2751234")  # ME
        words.append("32002E44B05C10000000021B7A0818200540BC9C5672277EFD30E7508479CBE9215D6AA469F53B42A5DB3AB6F120F2205D1234")  # ME
        words.append("32002E44B05C10000000021B7A08182005C2D901432A0617F274AFB0CAE42A0A6377F70AE1BB52C6A57301B49AC72CFAE41234")  # ME
        words.append("32002E44B05C10000000021B7A0A182005F9031AF7B93B04732C332EF55D20A3C7B5303F461486A8FC87AE4982A857BA751234")  # ME
        #words.append("32002E44B05C10000000021B7A0A1820050717C71E23B30C799B0E16ABFCDAD6A84487B368D58226382529656F0495BE961234")  # ME
    elif (demo_type == "aes_clean"):
        # BONEGA AES
        words.append("22001E44EE092101000001077A4F0010051AB94C4FDA694309E347E86FA437790C1234")  # ME
        words.append("22001E44EE092101000001067A4F0010051AB94C4FDA694309E347E86FA437790C6ED5")  # KZ
        # KAMSTRUP AES
        words.append("00005E442D2C9643636013047AD210500584535BEF5623858243FF4961635B6D30017FE12743EEC8D5757B0A3EC5E0BB052ABDBF71A75179A1340D01389E144F861F56780A3F8E1543E2368676A7BDC26214D2330757F0684421A3D5B1E4C781B84231")  # AH
    elif (demo_type == "clean"):
        # BONEGA
        words.append("22001E44EE092101000001067A4F0010002F2F04131A220000046D0328C4162F2F6ED5")  # ME
        words.append("22001E44EE092101000001077A4F0010002F2F04131A220000046D0328C4162F2F6ED5")  # ME
        # WEPTECH
        words.append("32002E44B05C11000000021B7A920800002F2F0A6667020AFB1A560402FD971D01002F2F2F2F2F2F2F2F2F2F2F2F2F2F2F1234")  # KZ
        words.append("32002e44b05c10000000021b7a660800002f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f8769")  # ME
        # KAMSTUP
        words.append("00005E442D2C9643636013047AD21000002F2F0422BA11000004140F000000043B0000000002FD1700100259A50A026CB316426CBF1544140F000000040F02000000025DAF0A04FF070600000004FF0802000000440F020000002F2F2F2F2F2F2F1234")  # AH
        # ZPA
        words.append("00002A44016A4493671201027244936712016A01020000002086108300762385010000862083009731920000001234")  # KZ
        words.append("00002A44016A4742750101027247427501016A01020000002086108300B80B0000000086208300F82A000000009658")  # PM
        words.append("2e002a44016a4742750101027247427501016a01021b00002086108300b80b0000000086208300f82a000000008cd4")  # JA
    return words

############### Vypocitani RSSI v dBm z (-3,-4) ########################################################################
def get_signal_value(sensor_rssi):
    sensor_rssi = int(sensor_rssi, 16)
    sensor_rssi = (sensor_rssi / 2) - 130
    return str(sensor_rssi).rjust(6, ' ')

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

############## Otevreme uloziste: SQLite databazi + souborovy system ###################################################
try:
    db = sqlite3.connect('MainDatabase.db')
except NameError:
    output("ERROR: Database cannot be estabilished.")
try:
    global file
    file = open("MainLog.txt", "ab")
    file.write(
        bytes("########################   " + time.strftime("%d/%m/%Y  %H:%M:%S") + "   ########################\n",
              'UTF-8'))
except NameError:
    print("ERROR: Database cannot be estabilished.")

############### Overime jestli neficime v demo modu ####################################################################
demo_run=""
myopts, args = getopt.getopt(sys.argv[1:], "o:a:")
if (len(args) > 0):
    demo_run = True

############ Stanoveni jestli jsem v demo rezimu nebo parsuji prichozi telegramy a pak ty telegramy parsuj #############
if (demo_run == True):
    output("Running in demonstration (" + args[0] + ") mode.")
    words = get_demo_telegrams(args[0])
    wordLed = len(words)
    errors = ''
    for i in range(0, wordLed):
        parse_telegram(str(words[i]),args[0])
else:
    # Setup a serial port
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=19200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    output("Device is on AMA0: " + str(ser.isOpen()))

    # Wake up device
    ser.write("\x00\x00")
    output("Device is waked up: True")

    # Set as a sniffer
    ser.write("\x00\x00>0a:01\x0D")
    z = ser.readline()
    output("Device is set as Sniffer T: " + z)

    # Sniff all packets
    output("Sniffing now:")

    while True:
        readedstring = ''
        readedstring = ser.read(200)
        readedstring = binascii.hexlify(readedstring)
        readedstring = str(readedstring)

        if readedstring:
            parse_telegram(readedstring,args[0])

############ Ukoncime hrani ############################################################################################
try:
    ser.close()
except NameError:
    output("WARNING: Serial port not closed correctly.")
try:
    db.close()
except NameError:
    output("WARNING: Database not closed correctly.")
try:
    file.close()
except NameError:
    output("WARNING: File not closed correctly.")
