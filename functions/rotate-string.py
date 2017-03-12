#!/usr/bin/env python

def LSB(bytes):
    new = ""
    size = len(bytes)
    while (size>0):
        new = new + bytes[size-2:size]
        size=size-2

    return new

before = "00112233445566778899"
after = LSB(before)
print(before)
print(after)