#!/usr/bin/env python
from Crypto.Cipher import AES
import binascii
import os

# Nacti co je potreba
TELEGRAM_DECRYPTED = binascii.unhexlify('1AB94C4FDA694309E347E86FA437790C')
AES_KEY_IQRF = binascii.unhexlify('2B7E151628AED2A6ABF7158809CF4F3C')
AES_KEY_DEVICE = binascii.unhexlify('2B7E151628AED2A6ABF7158809CF4F3C')
AES_IV = binascii.unhexlify('EE092101000001064F4F4F4F4F4F4F4F')

# Vsechno nad velkymi pismeny
binascii.hexlify(AES_IV).upper()
binascii.hexlify(AES_KEY_IQRF).upper()
binascii.hexlify(AES_KEY_DEVICE).upper()
binascii.hexlify(TELEGRAM_DECRYPTED).upper()

# Vem telegram rozsifrovany univerzalnim klicem (AES klic zadany v IQRF) a zpet ho s nim zasifruj. Dostaneme sprave prenaseny telegram.
encryptor_back = AES.new(AES_KEY_IQRF, AES.MODE_CBC, IV=AES_IV)
TELEGRAM_CRYPTED = encryptor_back.encrypt(TELEGRAM_DECRYPTED)

# Ten ted rozsifrujeme spravnym klicem (AES klic daneho zarizeni), dostaneme nesifrovana data.
encryptor_new = AES.new(AES_KEY_DEVICE, AES.MODE_CBC, IV=AES_IV)
TELEGRAM_ORIGINAL = encryptor_new.decrypt(TELEGRAM_CRYPTED)

# Pro kontrolu to vypiseme
print(binascii.hexlify(TELEGRAM_DECRYPTED).upper())
print(binascii.hexlify(TELEGRAM_CRYPTED).upper())
print(binascii.hexlify(TELEGRAM_ORIGINAL).upper())
