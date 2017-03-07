#!/usr/bin/python
__author__ = 'nixCraft'
import sys, getopt

# Store input and output file names
ifile = ''
ofile = ''

# Read command line args
myopts, args = getopt.getopt(sys.argv[1:], "o:a:")

###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-p':
        used_port = a
    elif o == '-r':
        used_mode = a
    else:
        print("Usage: %s -p serial_port -r wmbus_mode" % sys.argv[0])

# Display input and output file name passed as the args
print("Serial port : %s and WmBus mode: %s" % (ifile, ofile))