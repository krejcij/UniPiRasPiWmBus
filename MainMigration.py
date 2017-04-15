#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import sqlite3
except ImportError:
    print("FATAL ERROR: SQite3 module not found !")
    exit(1)
try:
    import gspread
except ImportError:
    print("FATAL ERROR: GSpread module not found !")
    exit(1)
try:
    from oauth2client.service_account import ServiceAccountCredentials
except ImportError:
    print("FATAL ERROR: oauth2 module not found !")
    exit(1)

import time

global db
global file


############ Logovani do souboru #######################################################################################
def log(log):
    file.write(bytes(time.strftime("%d/%m/%Y  %H:%M:%S  ") + log + "\n", 'UTF-8'))
    return


############ Obecny vystup #############################################################################################
def output(output):
    log(output)
    print(time.strftime("%d/%m/%Y  %H:%M:%S  ") + output)
    return


############## Otevreme uloziste: SQLite databazi + souborovy system ###################################################
try:
    db = sqlite3.connect('MainDatabase.db')
except NameError:
    output("ERROR: Database cannot be estabilished.")
try:
    file = open("MigrationLog.txt", "ab")
    file.write(
        bytes("########################   " + time.strftime("%d/%m/%Y  %H:%M:%S") + "   ########################\n",
              'UTF-8'))
except NameError:
    print("ERROR: Log file cannot be estabilished.")

############## Autorizujeme GoogleAPI ##################################################################################
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('./settings/GoogleSpreadSheetAccount.json', scope)
client = gspread.authorize(creds)

############## Mrkneme se do databaze co mame k dispozici za zarizeni
with db:
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    cur.execute("SELECT `DEVICE_INFO`,`DEVICE_ADDRESS` FROM `DEVICES` ORDER BY `DEVICE_INFO` ASC LIMIT 0, 50000;")
    devices = cur.fetchall()
    for device in devices:
        ############## Zalozime dokument daneho zarizen a urcitymi pravy pokud neexistuje, jinak ho otevreme
        dokument_name = device["DEVICE_ADDRESS"]
        try:
            DOKUMENT = client.open(dokument_name)
            output('Otevren dokument ' + dokument_name)
        except gspread.exceptions.SpreadsheetNotFound:
            DOKUMENT = client.create(dokument_name)
            output('Zalozen dokument ' + dokument_name)
            client.insert_permission(DOKUMENT.id, 'UniPiRasPiWmBus@gmail.com', perm_type='user', role='owner')
            client.insert_permission(DOKUMENT.id, 'hanes.tuky@gmail.com', perm_type='user', role='writer')
            client.insert_permission(DOKUMENT.id, None, perm_type='anyone', role='reader')
            output('    Dokumentu ' + dokument_name + ' udeleny odpovidajici pristupova prava')
            ############## Mrkneme se do databaze co dane zarizeni nacetlo za poslednich 24 hodin
            with db:
                db.row_factory = sqlite3.Row
                cur = db.cursor()
                cur.execute("SELECT  DATETIME, VALUE1, VALUE2 FROM `MEASURES` WHERE `DEVICE` LIKE '%"+device["DEVICE_ADDRESS"]+"%' ORDER BY `DATETIME` ASC")
                values = cur.fetchall()
                ############## A do daneho dokumentu vytvorime list pokud naaaahodou neexistuje, jinak problem
                list_name = time.strftime("%d/%m/%Y  %H:%M:%S")
                try:
                    LIST = DOKUMENT.add_worksheet(list_name, 1, 3)
                    output('    Zalozen list ' + list_name + ' v dokumentu ' + dokument_name)
                except gspread.exceptions.RequestError:
                    output('    ERROR: Kolize pri zakladani listu ' + list_name + ' v dokumentu ' + dokument_name)
                for value in values:
                    print("%s %s %s" % (value["DATETIME"], value["VALUE1"], value["VALUE2"]))
                    ############## A ten list ted proste naplnime datama
                    try:
                        LIST.append_row([value["DATETIME"], value["VALUE1"], value["VALUE2"]])
                        output('        Vlozen radek: ' + value["DATETIME"] + ',' + value["VALUE1"]+ ',' + value["VALUE2"])
                    except NameError:
                        output('        ERROR: Kolize pri zapisu na list ' + list_name + ' v dokumentu ' + dokument_name)

############## Funkce pro pripadne overeni ze se tam nahralo co melo
# list_of_hashes = DOKUMENT.get_all_records()
# print(list_of_hashes)

############ Ukoncime hrani ############################################################################################
try:
    db.close()
except NameError:
    output("WARNING: Database not closed correctly.")
try:
    file.close()
except NameError:
    output("WARNING: File not closed correctly.")
