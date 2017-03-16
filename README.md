# Python script used for reading WmBUS telegrams with IQRF module implanted on UniPi module for RaspberryPi

### How to use

Skript can be run in Python interpreter:
+ General usage of the script: **python MainApplication.py**
+ Demo mode for encrypted packets from IQRF: *python MainApplication.py aes_iqrf*
+ Demo mode for general encrypted packets: *python MainApplication.py aes_clean*
+ Demo mode for other normal packets: *python MainApplication.py clean*

### Example

![Screen](./MainExample.png)

### Wishlist
+ Add Kamstrup parsing structure
+ Add Pikkerton parsing structure
+ Add encrypt/decrypt function
+ Finalize parsing Bonega values and time
+ Repair daily log dividing
+ Create export application
+ Create data visualisation
+ Create rapsi apache website
+ Run this app as a service
+ Create instalation script