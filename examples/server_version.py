#!/usr/bin/env python
# server_version.py - retrieve and display database server version
import cgitb
cgitb.enable()

import MySQLdb


conn = MySQLdb.connect (host = "localhost",
                       user = "root",
                       passwd = "",
                       db = "honor_thyself")
cursor = conn.cursor ()
cursor.execute ("SELECT VERSION()")
row = cursor.fetchone ()
print("Content-Type: text/html\n")

print("server version:", row[0])
cursor.close ()
conn.close ()
