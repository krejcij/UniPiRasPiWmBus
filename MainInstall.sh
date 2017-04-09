#!/bin/sh
sudo su -

# Vsechno vyupdatovat
apt-get update -y
apt-get upgrade -y
apt-get dist-upgrade -y

# Nastavit konfiguraky
    # enable-uart
    # console=tty
    # dt-overlay=pi3
    # povolit ssh
    
# Nainstalit balicky
apt-get install python-dev python-crypto sqlite3 apache2 git mc python-serial php -y

# Stahnout dvakrat repozitar
    # Nastavit prava na spousteni skriptu
    # Nastavit prava pro zapis souboru
    # Vytvorit symlink do BINu
    # Vytvorit symlinky pro logy a db

     
