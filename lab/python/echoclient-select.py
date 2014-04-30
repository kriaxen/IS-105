# -*- coding: latin-1 -*-

"""
Poker klient utvikles her
Dette eksemplet gir mulighet til å sende flere kommandoer gjennom socketen
Man kan avslutte forbindelse med å sende en tom linje
"""

import socket
import sys


host = 'localhost'
port = 10000
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
sys.stdout.write('%')

while 1:
    # lese fra tastaturet (må finne på kommandoer)
	# kan droppe feilsjekking i denne versjonen
    line = sys.stdin.readline()
    if line == '\n':
        break
    s.send(line)
	
    data = s.recv(size)
	
    sys.stdout.write(data)
    sys.stdout.write('%')
s.close()
