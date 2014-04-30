# -*- coding: latin-1 -*-

import socket
import sys

messages = ['Dette er en melding. ',
			'Den vil blir sent ',
			'i deler.',
			]
server_address = ('localhost', 10000)

# Lage flere TCP/IP sockets
socks = [ socket.socket(socket.AF_INET, socket.SOCK_STREAM),
		socket.socket(socket.AF_INET, socket.SOCK_STREAM),
		]

# Koble til porten som serveren hører på
print >>sys.stderr, 'kobler til %s port %s' % server_address
for s in socks:
	s.connect(server_address)

# Så sender en del av meldingen av gangen gjennom hver socket og 
# leser alle responsene etter at ny data er skrevet
for message in messages:

	# Send meldinger på begge socketene
	for s in socks:
		print >>sys.stderr, '%s: sender "%s"' % (s.getsockname(), message)
		s.send(message)

	# Lese responsene fra begge socketene
	for s in socks:
		data = s.recv(1024)
		print >>sys.stderr, '%s: mottok "%s"' % (s.getsockname(), data)
		if not data:
			print >>sys.stderr, 'lukker socketen', s.getsockname()
			s.close()
