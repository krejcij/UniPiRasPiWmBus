#!/usr/bin/env python
import sqlite3

conn = sqlite3.connect('MainDatabase.db')
print("Opened database successfully")

conn.close()


