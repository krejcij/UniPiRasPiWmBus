#!/bin/sh
sudo su -

# Vsechno vyupdatovat
apt-get update -y
apt-get upgrade -y
apt-get dist-upgrade -y

# Nastavit konfiguraky
    # enable-uart=1
    # console=tty
    # dt-overlay=pi3
    
# Nainstalit balicky
apt-get install python-dev python-crypto python-serial sqlite3 apache2 php libapache2-mod-php git mc htop -y

# Stahnout repozitar aplikace
git clone https://github.com/krejcij/UniPiRasPiWmBus.git /var/www/html.

# Nastavit prava na spousteni skriptu
chmod +x /var/www/html/MainProgram.sh

# Nastavit prava pro zapis souboru
chmod +w /var/www/html/logs

# Vytvorit symlink do BINu
ln -s /var/www/html/MainProgram.sh /usr/bin/
  
# Nastavit spousteni po startu systemu
ln -s /var/www/html/MainProgram.sh /etc/rc.d/
ln -s /var/www/html/MainProgram.sh /etc/init.d/